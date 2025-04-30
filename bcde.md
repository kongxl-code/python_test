# 更高效的多进程解压tar.gz文件方案

要更高效地从同一个tar.gz文件中提取文件，我们需要解决几个关键问题：
1. 避免重复解压整个tar文件
2. 减少进程间竞争和I/O冲突
3. 利用现代硬件并行能力

## 高效替代方案1：使用内存映射和共享内存

```python
import mmap
import os
import tarfile
import multiprocessing
from functools import partial

def extract_worker(shared_name, member_info, output_dir):
    """使用内存映射共享的tar文件进行提取"""
    try:
        # 访问共享内存中的tar文件
        with open(shared_name, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                with tarfile.open(fileobj=mm, mode='r:*') as tar:
                    tar.extract(member_info, path=output_dir)
        print(f"Extracted: {member_info.name}")
    except Exception as e:
        print(f"Error extracting {member_info.name}: {str(e)}")

def efficient_parallel_extract(tar_path, output_dir, num_processes=None):
    """高效并行提取"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建临时共享文件（实际项目中应考虑更安全的临时文件处理）
    shared_name = "/dev/shm/temp_shared.tar" if os.path.exists("/dev/shm") else "temp_shared.tar"
    os.system(f"cp {tar_path} {shared_name}")
    
    try:
        # 获取成员信息
        with tarfile.open(tar_path, 'r:*') as tar:
            members = [m for m in tar.getmembers() if m.isfile()]
        
        # 设置进程数
        num_processes = num_processes or multiprocessing.cpu_count()
        
        # 创建进程池
        with multiprocessing.Pool(processes=num_processes) as pool:
            # 使用partial固定共享文件名和输出目录
            func = partial(extract_worker, shared_name, output_dir=output_dir)
            pool.map(func, members)
    finally:
        # 清理临时文件
        if os.path.exists(shared_name):
            os.remove(shared_name)

if __name__ == '__main__':
    efficient_parallel_extract('large_file.tar.gz', 'extracted_files')
```

## 高效替代方案2：使用libarchive（更底层的C库）

```python
# 需要先安装: pip install libarchive-c
import libarchive
import multiprocessing
import os

def libarchive_extract_worker(entry, output_dir):
    """使用libarchive提取单个文件"""
    try:
        path = os.path.join(output_dir, entry.pathname)
        if entry.isdir:
            os.makedirs(path, exist_ok=True)
        elif entry.isfile:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)
        print(f"Extracted: {entry.pathname}")
    except Exception as e:
        print(f"Error extracting {entry.pathname}: {str(e)}")

def parallel_libarchive_extract(tar_path, output_dir, num_processes=None):
    """使用libarchive并行提取"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取所有条目信息
    entries = []
    with libarchive.file_reader(tar_path) as archive:
        for entry in archive:
            entries.append(entry)
    
    # 设置进程数
    num_processes = num_processes or multiprocessing.cpu_count()
    
    # 创建进程池
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.starmap(libarchive_extract_worker, [(e, output_dir) for e in entries])

if __name__ == '__main__':
    parallel_libarchive_extract('large_file.tar.gz', 'extracted_files_libarchive')
```

## 高效替代方案3：使用多进程管道通信

```python
import tarfile
import multiprocessing
import os
from io import BytesIO

def pipe_worker(conn, output_dir):
    """通过管道接收文件数据并写入"""
    while True:
        member_info, data = conn.recv()
        if member_info is None:  # 结束信号
            break
        
        try:
            path = os.path.join(output_dir, member_info.name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(data)
            print(f"Extracted: {member_info.name}")
        except Exception as e:
            print(f"Error extracting {member_info.name}: {str(e)}")

def parallel_pipe_extract(tar_path, output_dir, num_processes=4):
    """使用管道通信的并行提取"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 创建进程和管道
    parent_conns = []
    processes = []
    for _ in range(num_processes):
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(
            target=pipe_worker, 
            args=(child_conn, output_dir)
        )
        p.start()
        processes.append(p)
        parent_conns.append(parent_conn)
    
    try:
        # 主进程读取tar文件并分发任务
        with tarfile.open(tar_path, 'r:*') as tar:
            for i, member in enumerate(tar.getmembers()):
                if not member.isfile():
                    continue
                
                # 选择worker（简单轮询）
                conn = parent_conns[i % num_processes]
                # 读取文件数据
                f = tar.extractfile(member)
                data = f.read()
                conn.send((member, data))
    finally:
        # 发送结束信号
        for conn in parent_conns:
            conn.send((None, None))
        
        # 等待所有进程结束
        for p in processes:
            p.join()

if __name__ == '__main__':
    parallel_pipe_extract('large_file.tar.gz', 'extracted_files_pipe')
```

## 性能对比和选择建议

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 内存映射 | 减少I/O操作，高效共享数据 | 需要足够内存，临时文件处理 | 大文件，内存充足系统 |
| libarchive | 底层C库，性能最优 | 额外依赖，API较底层 | 极致性能需求 |
| 管道通信 | 避免磁盘I/O瓶颈 | 实现复杂，内存使用高 | 中等大小文件 |

**最佳实践建议**：
1. 对于Linux系统，优先考虑方案1（内存映射），使用`/dev/shm`实现真正的内存共享
2. 如果需要最佳性能且可接受外部依赖，使用方案2（libarchive）
3. 对于Windows系统或需要更精细控制的情况，考虑方案3（管道通信）
4. 无论哪种方案，都应根据实际文件数量和大小调整进程数（通常CPU核心数的1-2倍）

这些方案都避免了重复解压整个tar文件的问题，通过不同的共享机制实现了真正高效的并行提取。
