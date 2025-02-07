// src/stores/customTablesStore.js
import create from 'zustand';
import { v4 as uuidv4 } from 'uuid'

const useCustomTablesStore = create((set, get) => ({
  customTables: [],

  addCustomTable: (template = '') => {
    set((state) => ({
      customTables: [
        ...state.customTables,
        {
          id: uuidv4(),
          title: template || 'New Table',
          headers: [
            {
              id: uuidv4(),
              columns: [
                {
                  id: uuidv4(),
                  header: '',
                  type: 'text'
                }
              ]
            }
          ],
          rows: []
        }
      ]
    }))
  },

  updateTableTitle: (tableId, newTitle) => {
    set((state) => ({
      customTables: state.customTables.map((table) =>
        table.id === tableId ? { ...table, title: newTitle } : table
      )
    }))
  },

  removeCustomTable: (tableId) => {
    set((state) => ({
      customTables: state.customTables.filter((table) => table.id !== tableId)
    }))
  },

  addHeaderRow: (tableId) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: [
              ...table.headers,
              {
                id: uuidv4(),
                columns: table.headers[0].columns.map((col) => ({
                  id: uuidv4(),
                  header: '',
                  type: col.type
                }))
              }
            ]
          }
        }
        return table
      })
    }))
  },

  addColumn: (tableId) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: table.headers.map((headerRow) => ({
              ...headerRow,
              columns: [
                ...headerRow.columns,
                {
                  id: uuidv4(),
                  header: '',
                  type: 'text'
                }
              ]
            }))
          }
        }
        return table
      })
    }))
  },

  addRow: (tableId) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          const newRow = {
            id: uuidv4()
          }
          return {
            ...table,
            rows: [...table.rows, newRow]
          }
        }
        return table
      })
    }))
  },

  updateHeaderValue: (tableId, headerRowId, columnId, value) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: table.headers.map((headerRow) => {
              if (headerRow.id === headerRowId) {
                return {
                  ...headerRow,
                  columns: headerRow.columns.map((col) =>
                    col.id === columnId ? { ...col, header: value } : col
                  )
                }
              }
              return headerRow
            })
          }
        }
        return table
      })
    }))
  },

  removeColumn: (tableId, columnIndex) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: table.headers.map((headerRow) => ({
              ...headerRow,
              columns: headerRow.columns.filter((_, idx) => idx !== columnIndex)
            }))
          }
        }
        return table
      })
    }))
  },

  updateColumn: (tableId, columnId, field, value) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: table.headers.map((headerRow) => ({
              ...headerRow,
              columns: headerRow.columns.map((col) =>
                col.id === columnId ? { ...col, [field]: value } : col
              )
            }))
          }
        }
        return table
      })
    }))
  },

  removeHeaderRow: (tableId, headerRowId) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            headers: table.headers.filter((headerRow) => headerRow.id !== headerRowId)
          }
        }
        return table
      })
    }))
  },

  updateCellValue: (tableId, rowIndex, columnId, value) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            rows: table.rows.map((row, idx) => {
              if (idx === rowIndex) {
                return {
                  ...row,
                  [columnId]: value
                }
              }
              return row
            })
          }
        }
        return table
      })
    }))
  },

  removeRow: (tableId, rowIndex) => {
    set((state) => ({
      customTables: state.customTables.map((table) => {
        if (table.id === tableId) {
          return {
            ...table,
            rows: table.rows.filter((_, idx) => idx !== rowIndex)
          }
        }
        return table
      })
    }))
  }
}))

export default useCustomTablesStore