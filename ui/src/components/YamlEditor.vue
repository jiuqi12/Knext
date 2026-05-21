<script setup>
import { ref, onMounted, onUnmounted, watch, shallowRef } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { EditorState } from '@codemirror/state'
import { yaml } from '@codemirror/lang-yaml'
import { oneDark } from '@codemirror/theme-one-dark'
import { linter, lintGutter } from '@codemirror/lint'
import yamlParser from 'js-yaml'
import { yamlTemplates, templateCategories } from '@/utils/yamlTemplate.js'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  readOnly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const editorRef = ref(null)
const view = shallowRef(null)
const error = ref('')

const selectedTemplate = ref('')

const applyTemplate = (type) => {
  const template = yamlTemplates[type]

  if (!template) return

  view.value.dispatch({
    changes: {
      from: 0,
      to: view.value.state.doc.length,
      insert: template
    }
  })
  selectedTemplate.value = ''
}

// 防止循环更新的标志位
let isUpdatingFromProps = false

// YAML linter - 检查语法错误
const yamlLinter = linter((view) => {
  const doc = view.state.doc.toString()
  if (!doc.trim()) return []

  try {
    yamlParser.load(doc)
    error.value = ''
    return []
  } catch (e) {
    const line = e.mark ? e.mark.line + 1 : 1
    const col = e.mark ? e.mark.column + 1 : 1
    error.value = `第 ${line} 行，第 ${col} 列: ${e.reason}`

    return [
      {
        from: e.mark ? e.mark.position : 0,
        to: e.mark ? e.mark.position + 1 : 1,
        severity: 'error',
        message: e.reason
      }
    ]
  }
})

// 更新编辑器内容
const updateEditorContent = (newContent) => {
  if (!view.value) return

  const currentContent = view.value.state.doc.toString()
  if (newContent !== currentContent) {
    isUpdatingFromProps = true
    view.value.dispatch({
      changes: {
        from: 0,
        to: currentContent.length,
        insert: newContent
      }
    })
    isUpdatingFromProps = false
  }
}

// 格式化 YAML
const formatYaml = () => {
  if (!view.value) return

  try {
    const content = view.value.state.doc.toString()
    const parsed = yamlParser.load(content)
    const formatted = yamlParser.dump(parsed, {
      indent: 2,
      lineWidth: 120,
      noRefs: true
    })

    updateEditorContent(formatted)
    error.value = ''
  } catch {
    error.value = 'YAML 格式错误，无法格式化'
  }
}

// 初始化编辑器
onMounted(() => {
  if (!editorRef.value) return

  const state = EditorState.create({
    doc: props.modelValue || '',
    extensions: [
      basicSetup,
      yaml(),
      oneDark,
      yamlLinter,
      lintGutter(),
      EditorView.updateListener.of((update) => {
        if (update.docChanged && !isUpdatingFromProps) {
          const value = update.state.doc.toString()
          emit('update:modelValue', value)
        }
      }),
      EditorState.readOnly.of(props.readOnly),
      EditorView.theme({
        '&': {
          height: '100%',
          fontSize: '14px'
        },
        '.cm-scroller': {
          fontFamily: 'Consolas, "Courier New", monospace',
          overflow: 'auto'
        },
        '.cm-content': {
          minHeight: '400px'
        },
        '.cm-gutters': {
          backgroundColor: '#1e1e1e',
          color: '#858585',
          border: 'none'
        },
        '.cm-activeLineGutter': {
          backgroundColor: '#2c2c2c'
        },
        '.cm-activeLine': {
          backgroundColor: 'rgba(255, 255, 255, 0.05)'
        },
        '.cm-cursor': {
          borderLeftColor: '#fff'
        },
        '.cm-selectionBackground': {
          backgroundColor: 'rgba(255, 255, 255, 0.2) !important'
        }
      })
    ]
  })

  view.value = new EditorView({
    state,
    parent: editorRef.value
  })
})

// 监听外部 modelValue 变化
watch(
  () => props.modelValue,
  (newVal) => {
    updateEditorContent(newVal || '')
  }
)

// 监听 readOnly 变化
watch(
  () => props.readOnly,
  (newReadOnly) => {
    if (view.value) {
      const content = view.value.state.doc.toString()
      view.value.destroy()

      const state = EditorState.create({
        doc: content,
        extensions: [
          basicSetup,
          yaml(),
          oneDark,
          yamlLinter,
          lintGutter(),
          EditorView.updateListener.of((update) => {
            if (update.docChanged && !isUpdatingFromProps) {
              const value = update.state.doc.toString()
              emit('update:modelValue', value)
            }
          }),
          EditorState.readOnly.of(newReadOnly),
          EditorView.theme({
            '&': {
              height: '100%',
              fontSize: '14px'
            },
            '.cm-scroller': {
              fontFamily: 'Consolas, "Courier New", monospace',
              overflow: 'auto'
            },
            '.cm-content': {
              minHeight: '400px'
            },
            '.cm-gutters': {
              backgroundColor: '#1e1e1e',
              color: '#858585',
              border: 'none'
            },
            '.cm-activeLineGutter': {
              backgroundColor: '#2c2c2c'
            },
            '.cm-activeLine': {
              backgroundColor: 'rgba(255, 255, 255, 0.05)'
            },
            '.cm-cursor': {
              borderLeftColor: '#fff'
            },
            '.cm-selectionBackground': {
              backgroundColor: 'rgba(255, 255, 255, 0.2) !important'
            }
          })
        ]
      })

      view.value = new EditorView({
        state,
        parent: editorRef.value
      })
    }
  }
)

// 组件卸载时销毁编辑器
onUnmounted(() => {
  if (view.value) {
    view.value.destroy()
    view.value = null
  }
})

// 校验 YAML 内容
const validate = () => {
  const doc = view.value?.state.doc.toString()
  if (!doc?.trim()) {
    error.value = 'YAML 内容不能为空'
    return false
  }
  try {
    yamlParser.load(doc)
    error.value = ''
    return true
  } catch (e) {
    const line = e.mark ? e.mark.line + 1 : 1
    const col = e.mark ? e.mark.column + 1 : 1
    error.value = `第 ${line} 行，第 ${col} 列: ${e.reason}`
    return false
  }
}

// 暴露方法供父组件调用
defineExpose({
  formatYaml,
  validate,
  error,
  getEditorView: () => view.value
})
</script>

<template>
  <div class="yaml-editor">
    <div class="editor-header">
      <div class="header-left">
        <span class="header-label">YAML 编辑器</span>
        <el-select
          v-model="selectedTemplate"
          placeholder="加载模板"
          class="template-select"
          @change="applyTemplate"
        >
          <el-option-group
            v-for="category in templateCategories"
            :key="category.label"
            :label="category.label"
          >
            <el-option
              v-for="item in category.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-option-group>
        </el-select>
      </div>
      <div class="header-right">
        <span v-if="error" class="error-text">
          <el-icon><WarningFilled /></el-icon>
          {{ error }}
        </span>
        <el-button size="small" @click="formatYaml" class="format-btn">
          <el-icon><EditPen /></el-icon>
          格式化
        </el-button>
      </div>
    </div>
    <div class="editor-container">
      <div class="editor" ref="editorRef"></div>
    </div>
  </div>
</template>

<style scoped>
.yaml-editor {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #1e1e2e;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: linear-gradient(135deg, #2b2d42 0%, #1e1e2e 100%);
  border-bottom: 1px solid #333;
  flex-shrink: 0;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-label {
  color: #a6adc8;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.template-select {
  width: 180px;
}

.template-select :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  box-shadow: none;
}

.template-select :deep(.el-input__inner) {
  color: #cdd6f4;
  font-size: 13px;
}

.template-select :deep(.el-input__inner::placeholder) {
  color: #6c7086;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.error-text {
  color: #f38ba8;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.format-btn {
  background: rgba(137, 180, 250, 0.12) !important;
  border: 1px solid rgba(137, 180, 250, 0.25) !important;
  color: #89b4fa !important;
  border-radius: 6px !important;
  font-weight: 500;
  transition: all 0.2s ease;
}

.format-btn:hover {
  background: rgba(137, 180, 250, 0.22) !important;
  border-color: rgba(137, 180, 250, 0.45) !important;
  transform: translateY(-1px);
}

.editor-container {
  flex: 1;
  overflow: hidden;
}

.editor {
  height: 100%;
}

.editor :deep(.cm-editor) {
  height: 100%;
}

.editor :deep(.cm-scroller) {
  height: 100%;
  font-family:
    'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, 'Courier New',
    monospace;
}
</style>
