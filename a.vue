<template>
  <div class="app-container">
    <el-table :data="tableData" style="width: 100%">
      <!-- Step Name 列 -->
      <el-table-column prop="step_name" label="Step Name" width="180" />
      
      <!-- State Name 列 -->
      <el-table-column prop="state_name" label="State Name" width="180" />
      
      <!-- Thresholds 列 -->
      <el-table-column label="Thresholds (UTC)">
        <template #default="{ row }">
          <span v-if="!row.editing">{{ formatTime(row.thresholds) }}</span>
          <el-time-picker
            v-else
            v-model="row.editThresholds"
            format="HH:mm:ss"
            value-format="HH:mm:ss"
            placeholder="选择时间"
          />
        </template>
      </el-table-column>
      
      <!-- 操作列 -->
      <el-table-column label="操作" width="180">
        <template #default="{ row, $index }">
          <template v-if="!row.editing">
            <el-button size="small" @click="handleEdit(row, $index)">
              编辑
            </el-button>
          </template>
          <template v-else>
            <el-button size="small" type="success" @click="handleSave(row, $index)">
              保存
            </el-button>
            <el-button size="small" @click="handleCancel(row, $index)">
              取消
            </el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 示例数据
const tableData = ref([
  {
    step_name: 'Step 1',
    state_name: 'State A',
    thresholds: 3600000, // 1小时
    editing: false,
    editThresholds: ''
  },
  {
    step_name: 'Step 2',
    state_name: 'State B',
    thresholds: 7200000, // 2小时
    editing: false,
    editThresholds: ''
  },
  {
    step_name: 'Step 3',
    state_name: 'State C',
    thresholds: 10800000, // 3小时
    editing: false,
    editThresholds: ''
  }
]);

// 格式化毫秒为 HH:mm:ss
const formatTime = (milliseconds) => {
  const date = new Date(milliseconds);
  return date.toISOString().substr(11, 8);
};

// 编辑操作
const handleEdit = (row, index) => {
  // 将毫秒转换为 HH:mm:ss 格式用于编辑
  const date = new Date(row.thresholds);
  row.editThresholds = date.toISOString().substr(11, 8);
  tableData.value[index].editing = true;
};

// 保存操作
const handleSave = (row, index) => {
  // 将 HH:mm:ss 转换回毫秒
  const [hours, minutes, seconds] = row.editThresholds.split(':').map(Number);
  const totalMilliseconds = (hours * 3600 + minutes * 60 + seconds) * 1000;
  
  tableData.value[index].thresholds = totalMilliseconds;
  tableData.value[index].editing = false;
};

// 取消操作
const handleCancel = (row, index) => {
  tableData.value[index].editing = false;
};
</script>

<style scoped>
.app-container {
  padding: 20px;
}
</style>
