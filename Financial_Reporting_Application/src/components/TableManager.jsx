import React, { useState, useEffect, useCallback} from 'react';
import { Edit, Plus, Save, Trash, AlertCircle, Printer, FileText } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Alert, AlertTitle, AlertDescription } from './ui/alert';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from './ui/alert-dialog';

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from './ui/card';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import { jsPDF } from 'jspdf';
import autoTable from 'jspdf-autotable';
import { Button } from './ui/button';
import { Input } from './ui/input';

const TableManager = () => {
  const [tables, setTables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sqlNameError, setSqlNameError] = useState('');
  const [selectedTable, setSelectedTable] = useState('');
  const [tableData, setTableData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [selectedHeader, setSelectedHeader] = useState('');
  const [headerValue, setHeaderValue] = useState(0);
  const [selectedValue, setSelectedValue] = useState('');
  const [headerValues, setHeaderValues] = useState([]);
  const [monthlyError, setMonthlyError] = useState('');
  const [editingCell, setEditingCell] = useState(null);
  const [editValue, setEditValue] = useState('');
  const [monthlyTable, setMonthlyTable] = useState(null);
  const [isMonthlyTableValid, setIsMonthlyTableValid] = useState(false);
  const [monthlyData, setMonthlyData] = useState({});
  const [tableName, setTableName] = useState('');
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const [isSaving, setIsSaving] = useState(false);

  // Fetch available tables
  useEffect(() => {
    const fetchTables = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('http://localhost:5000/api/tables');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        if (Array.isArray(data)) {
          setTables(data);
        } else {
          setError('Invalid data format received from server');
        }
      } catch (error) {
        console.error('Error fetching tables:', error);
        setError('Failed to fetch tables. Please check if the backend server is running.');
      } finally {
        setLoading(false);
      }
    };
    fetchTables();
  }, []);

  // Fetch table data
  const fetchTableData = useCallback(async () => {
    if (!selectedTable) return;

    try {
      const response = await fetch(`http://localhost:5000/api/tableData/${selectedTable}`);
      const data = await response.json();
      
      setTableData(data);
      if (data.length > 0) {
        setHeaders(Object.keys(data[0]));
      }
    } catch (error) {
      console.error('Error fetching table data:', error);
      setError('Failed to fetch table data');
    }
  }, [selectedTable]);

  useEffect(() => {
    if (selectedTable) {
      fetchTableData();
    }
  }, [selectedTable, fetchTableData]);

  const handleCellEdit = async () => {
    if (!editingCell) return;

    try {
      const response = await fetch('http://localhost:5000/api/updateCell', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          table: selectedTable,
          id: editingCell.rowId,
          column: editingCell.header,
          value: editValue
        })
      });

      if (response.ok) {
        await fetchTableData();
      }
    } catch (error) {
      console.error('Error updating cell:', error);
      setError('Failed to update cell');
    }

    setEditingCell(null);
    setEditValue('');
  };

  const handleDeleteRow = async (id) => {
    try {
      const response = await fetch('http://localhost:5000/api/deleteRow', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          table: selectedTable,
          id: id
        })
      });

      if (response.ok) {
        await fetchTableData();
      }
    } catch (error) {
      console.error('Error deleting row:', error);
      setError('Failed to delete row');
    }
  };

  const handleDropTable = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/dropTable/${selectedTable}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setSelectedTable('');
        setTableData([]);
        setHeaders([]);
        setTables(tables.filter(t => t !== selectedTable));
      }
    } catch (error) {
      console.error('Error dropping table:', error);
      setError('Failed to drop table');
    }
  };

  // Helper function to check if a value is numeric
  const isNumeric = (value) => {
    if (typeof value === 'number') return true;
    if (typeof value === 'string') {
      const num = Number(value);
      return !isNaN(num) && !isNaN(parseFloat(value));
    }
    return false;
  };

  // Get numeric headers excluding 'id'
  const getNumericHeaders = () => {
    if (!tableData.length) return [];
    return headers.filter(header => {
      if (header === 'id') return false;
      const firstValue = tableData[0][header];
      return isNumeric(firstValue);
    });
  };

  // Update header selection to include value
  const handleHeaderSelect = (header) => {
    setSelectedHeader(header);
    setSelectedValue(''); // Reset selected value when header changes
    
    // Get unique values for the selected header
    const uniqueValues = [...new Set(tableData.map(row => row[header]))];
    setHeaderValues(uniqueValues);
    setMonthlyError('');
    setMonthlyData(Object.fromEntries(months.map(month => [month, 0])));
  };

  // Add handler for value selection
  const handleValueSelect = (value) => {
    setSelectedValue(value);
    setHeaderValue(parseFloat(value));
  };

  const createMonthlyTable = () => {
    if (!selectedHeader || !tableName) {
      setMonthlyError('Please select a header and enter a table name');
      return;
    }

    // Validate SQL safe name
    try {
      formatSqlSafeName(tableName);
      setSqlNameError(''); // Clear any previous SQL name errors
    } catch (error) {
      setSqlNameError(error.message);
      return;
    }

    // Calculate total of monthly values
    const total = Object.values(monthlyData).reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
    
    // Validate against header value
    if (total > headerValue) {
      setMonthlyError(`Total monthly values (${total.toFixed(2)}) cannot exceed the ${selectedHeader} value (${headerValue.toFixed(2)})`);
      setIsMonthlyTableValid(false);
      return;
    }

    const newData = {
      header: selectedHeader,
      tableName: tableName,
      headerValue: headerValue,
      months: { ...monthlyData },
      total: total,
      remaining: headerValue - total
    };

    setMonthlyTable(newData);
    setIsMonthlyTableValid(true);
    setMonthlyError('');
  };

  const validateMonthlyTable = useCallback(() => {
    if (!selectedHeader || !tableName) return false;
    
    const total = Object.values(monthlyData).reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
    return total <= headerValue;
  }, [selectedHeader, tableName, monthlyData, headerValue]);
  
  useEffect(() => {
    if (monthlyTable) {
      setIsMonthlyTableValid(validateMonthlyTable());
    }
  }, [monthlyTable, validateMonthlyTable]);

  // Modified monthly value change handler with validation
  const handleMonthlyValueChange = (month, value) => {
    const numValue = parseFloat(value) || 0;
    const newMonthlyData = {
      ...monthlyData,
      [month]: numValue
    };

    // Calculate total of all months
    const total = Object.values(newMonthlyData).reduce((sum, val) => sum + (parseFloat(val) || 0), 0);

    if (total > headerValue) {
      setMonthlyError(`Total monthly values (${total.toFixed(2)}) cannot exceed the ${selectedHeader} value (${headerValue.toFixed(2)})`);
    } else {
      setMonthlyError('');
    }

    setMonthlyData(newMonthlyData);
  };

  // Calculate remaining value
  const getRemainingValue = () => {
    const total = Object.values(monthlyData).reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
    return headerValue - total;
  };

  const chartData = months.map(month => ({
    name: month,
    value: monthlyData[month] || 0
  }));

  // Format table name for SQL safety
  const formatSqlSafeName = (name) => {
    const formatted = name
      .toLowerCase()
      .replace(/[^a-z0-9_]/g, '_')
      .replace(/^[^a-z]+/, '')
      .replace(/_{2,}/g, '_')
      .replace(/^_|_$/g, '')
      .substring(0, 63);

    if (!formatted) {
      throw new Error("Invalid table name. Table name must contain at least one letter.");
    }

    return formatted;
  };

  // Format column header for SQL
  const formatColumnHeader = (header) => {
    const formatted = formatSqlSafeName(header);
    return /^\d/.test(formatted) ? `col_${formatted}` : formatted;
  };

  const formatCellValue = (value, header) => {
    if (header === 'headers' && typeof value === 'string') {
      try {
        const parsedHeaders = JSON.parse(value);
        return parsedHeaders.map(h => h.name).join(', ');
      } catch (e) {
        return value;
      }
    }
    
    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value)) {
        return value.map(item => item.name).join(', ');
      }
      return JSON.stringify(value);
    }
    
    return value;
  };


  const handleSaveMonthlyTable = async () => {
    if (!monthlyTable || !isMonthlyTableValid) {
      setMonthlyError('Cannot save invalid monthly table');
      return;
    }

    // Validate SQL safe name before saving
    try {
      formatSqlSafeName(tableName);
    } catch (error) {
      setSqlNameError(error.message);
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      const monthlyTableData = {
        customTables: [{
          title: tableName,
          sqlSafeName: formatSqlSafeName(tableName),
          headers: [
            {
              name: 'month',
              sqlSafeName: 'month' // month sudah aman sebagai nama kolom SQL
            },
            {
              name: selectedHeader,
              sqlSafeName: formatColumnHeader(selectedHeader)
            }
          ],
          rows: months.map(month => ({
            month: month,
            [formatColumnHeader(selectedHeader)]: monthlyData[month] || 0
          }))
        }],
        budgetSections: []
      };

      console.log('Sending monthly table payload:', JSON.stringify(monthlyTableData, null, 2));

      const response = await fetch('http://localhost:5000/api/save-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(monthlyTableData)
      });

      if (!response.ok) {
        throw new Error('Failed to save monthly table');
      }

      setMonthlyError('');
      alert('Monthly table saved successfully!');
      
      const tablesResponse = await fetch('http://localhost:5000/api/tables');
      const tablesData = await tablesResponse.json();
      setTables(tablesData);

    } catch (error) {
      console.error('Save error:', error);
      setMonthlyError(`Failed to save monthly table: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };
  
  const printStyles = `
  /* Atur dasar printing */
  @media print {
    body {
      background: white !important;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
      color-adjust: exact !important;
    }

    /* Atur ukuran container utama */
    .printing {
      padding: 20px !important;
      max-width: 100% !important;
      margin: 0 !important;
      background: white !important;
    }

    /* Sembunyikan tombol-tombol yang tidak perlu */
    .printing button {
      display: none !important;
    }

    /* Atur tampilan input dan select */
    .printing input,
    .printing select {
      border: none !important;
      background: transparent !important;
      padding: 4px !important;
      font-size: 14px !important;
      color: black !important;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    /* Atur tampilan label */
    .printing label {
      color: #374151 !important;
      font-size: 12px !important;
      margin-bottom: 4px !important;
      display: block !important;
    }

    /* Atur tampilan section/card */
    .printing .bg-white {
      background: white !important;
      border: 1px solid #e5e7eb !important;
      box-shadow: none !important;
      margin-bottom: 16px !important;
      padding: 16px !important;
      page-break-inside: avoid !important;
    }

    /* Atur tampilan tabel */
    .printing table {
      width: 100% !important;
      border-collapse: collapse !important;
      margin-bottom: 16px !important;
      page-break-inside: avoid !important;
    }

    .printing table th,
    .printing table td {
      border: 1px solid #e5e7eb !important;
      padding: 8px !important;
      font-size: 12px !important;
      text-align: left !important;
    }

    .printing table th {
      background-color: #f3f4f6 !important;
      font-weight: 600 !important;
    }

    /* Atur tampilan header section */
    .printing h1 {
      font-size: 24px !important;
      margin-bottom: 20px !important;
      color: black !important;
    }

    .printing h2 {
      font-size: 18px !important;
      margin-bottom: 16px !important;
      color: black !important;
    }

    /* Atur tampilan grid */
    .printing .grid {
      display: grid !important;
      gap: 16px !important;
    }

    /* Atur tampilan total dan currency */
    .printing .text-right,
    .printing .font-bold {
      color: black !important;
      font-weight: bold !important;
    }

    /* Atur tampilan budget items */
    .printing .space-y-4 > div {
      margin-bottom: 12px !important;
    }

    /* Atur page breaks */
    .printing .page-break-before {
      page-break-before: always !important;
    }

    .printing .page-break-after {
      page-break-after: always !important;
    }

    /* Atur tampilan shadow */
    .printing .shadow,
    .printing .shadow-sm,
    .printing .shadow-md,
    .printing .shadow-lg {
      box-shadow: none !important;
    }

    /* Atur warna background */
    .printing .bg-blue-600,
    .printing .bg-green-600,
    .printing .bg-red-600 {
      background-color: transparent !important;
      color: black !important;
    }

    /* Atur tampilan readonly/disabled fields */
    .printing .bg-gray-50 {
      background-color: transparent !important;
      border: 1px solid #e5e7eb !important;
    }
  }
`;

  // Handle PDF generation
  const handlePDFExport = () => {
    if (!monthlyTable) return;

    const doc = new jsPDF();
    
    // Add title
    doc.setFontSize(16);
    doc.text(`Monthly ${selectedHeader} Data`, 14, 15);
    
    // Prepare table data
    const tableData = months.map(month => [
      month,
      monthlyData[month]?.toFixed(2) || '0.00'
    ]);
    
    // Add total row
    const total = Object.values(monthlyData).reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
    tableData.push(['Total', total.toFixed(2)]);

    // Generate table
    autoTable(doc, {
      head: [['Month', selectedHeader]],
      body: tableData,
      startY: 25,
      theme: 'grid',
      styles: {
        fontSize: 10,
        cellPadding: 3,
        textColor: [0, 0, 0], // Black text for all cells
        lineColor: [0, 0, 0], // Black borders
        lineWidth: 0.1,
      },
      headStyles: {
        fillColor: [255, 255, 255], // White background
        textColor: [0, 0, 0], // Black text
        halign: 'center', // Center-align header text
        fontStyle: 'bold',
      },
      bodyStyles: {
        halign: 'center', // Center-align body text
      },
    });

    // Get the final Y position after the table
    const finalY = doc.previousAutoTable.finalY || 150;

    // Add chart title
    doc.setFontSize(14);
    doc.text('Monthly Distribution Chart', 14, finalY + 15);

    // Convert chart SVG to canvas and add to PDF
    const chartElement = document.querySelector('.recharts-wrapper svg');
    if (chartElement) {
      const svgData = new XMLSerializer().serializeToString(chartElement);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        if (ctx) {
          ctx.drawImage(img, 0, 0);
          const imgData = canvas.toDataURL('image/png');
          doc.addImage(imgData, 'PNG', 14, finalY + 20, 180, 100);
        }
        doc.save(`${tableName}_monthly_data.pdf`);
      };

      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)));
    } else {
      doc.save(`${tableName}_monthly_data.pdf`);
    }
  };

  return (
    <>
      <style>{printStyles}</style>
      <div className="min-h-screen flex flex-col">
        {/* Header Section */}
        <div className="w-full bg-yellow-200">
          <div className="max-w-7xl mx-auto py-4 px-8 text-center">
            <h1 className="text-2xl font-bold">Table Manager</h1>
            <h2 className="text-muted-foreground font-bold">Manage and visualize your database tables</h2>
          </div>
        </div>

        {loading ? (
          <Card>
            <CardContent className="flex items-center justify-center h-32">
              <p>Loading tables...</p>
            </CardContent>
          </Card>
        ) : error ? (
          <Card>
            <CardContent className="p-6">
              <div className="text-red-500">
                {error}
                <div className="mt-2">
                  Please check:
                  <ul className="list-disc pl-5 mt-2">
                    <li>Backend server is running on http://localhost:5000</li>
                    <li>Database connection is working</li>
                    <li>API endpoints are correctly configured</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-8">
            {/* Table Selection Card */}
            <Card>
              <CardHeader>
                <CardTitle>Select Table</CardTitle>
                <CardDescription>Choose a table to view and manage its data</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 items-center">
                  <Select value={selectedTable} onValueChange={setSelectedTable}>
                    <SelectTrigger className="w-[280px] bg-white">
                      <SelectValue placeholder="Select table" />
                    </SelectTrigger>
                    <SelectContent className="bg-white z-50">
                      {tables.map((table) => (
                        <SelectItem key={table} value={table} className="hover:bg-gray-100">
                          {table}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  {selectedTable && (
                    <AlertDialog>
                      <AlertDialogTrigger asChild>
                        <Button variant="destructive" className="flex items-center gap-2">
                          <Trash className="h-4 w-4" />
                          Drop Table
                        </Button>
                      </AlertDialogTrigger>
                      <AlertDialogContent className="bg-white border shadow-lg">
                        <AlertDialogHeader>
                          <AlertDialogTitle className="text-gray-900">Drop Table</AlertDialogTitle>
                          <AlertDialogDescription className="text-gray-600">
                            Are you sure you want to drop this table? This action cannot be undone.
                          </AlertDialogDescription>
                        </AlertDialogHeader>
                        <AlertDialogFooter>
                          <AlertDialogCancel className="bg-gray-100 hover:bg-gray-200">Cancel</AlertDialogCancel>
                          <AlertDialogAction
                            onClick={handleDropTable}
                            className="bg-red-600 text-white hover:bg-red-700"
                          >
                            Continue
                          </AlertDialogAction>
                        </AlertDialogFooter>
                      </AlertDialogContent>
                    </AlertDialog>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Table Content Card */}
            {selectedTable && tableData.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>{selectedTable}</CardTitle>
                  <CardDescription>Table data and management</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="rounded-md border">
                    <Table>
                      <TableHeader>
                        <TableRow className="bg-muted/50">
                          {headers.map(header => (
                            <TableHead key={header} className="font-semibold">
                              {header}
                            </TableHead>
                          ))}
                          <TableHead>Actions</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {tableData.map((row, rowIndex) => (
                          <TableRow key={row.id || rowIndex} className="hover:bg-muted/50">
                            {headers.map(header => (
                              <TableCell key={`${row.id}-${header}`} className="p-4">
                                {editingCell?.rowId === row.id && editingCell?.header === header ? (
                                  <div className="flex gap-2">
                                    <Input
                                      value={editValue}
                                      onChange={(e) => setEditValue(e.target.value)}
                                      className="w-full"
                                    />
                                    <Button onClick={handleCellEdit}>
                                      <Save className="h-4 w-4" />
                                    </Button>
                                  </div>
                                ) : (
                                  <div 
                                    className="flex justify-between items-center cursor-pointer"
                                    onClick={() => {
                                      setEditingCell({ rowId: row.id, header });
                                      setEditValue(row[header]);
                                    }}
                                  >
                                    {formatCellValue(row[header], header)}
                                    <Edit className="h-4 w-4 opacity-50 hover:opacity-100" />
                                  </div>
                                )}
                              </TableCell>
                            ))}
                            <TableCell>
                              <Button
                                variant="destructive"
                                size="sm"
                                onClick={() => handleDeleteRow(row.id)}
                              >
                                <Trash className="h-4 w-4" />
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Monthly Data Card */}
            {selectedTable && (
              <Card>
                <CardHeader>
                  <CardTitle>Monthly Data Visualization</CardTitle>
                  <CardDescription>Create monthly data table and chart</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    <div className="flex gap-4 items-end">
                      {/* Header Selection */}
                      <div className="space-y-2">
                        <Select value={selectedHeader} onValueChange={handleHeaderSelect}>
                          <SelectTrigger className="w-[280px] bg-white">
                            <SelectValue placeholder="Select numeric header" />
                          </SelectTrigger>
                          <SelectContent className="bg-white z-50">
                            {getNumericHeaders().map(header => (
                              <SelectItem key={header} value={header}>
                                {header}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      {/* Value Selection - New Dropdown */}
                      {selectedHeader && (
                        <div className="space-y-2">
                          <Select value={selectedValue} onValueChange={handleValueSelect}>
                            <SelectTrigger className="w-[280px] bg-white">
                              <SelectValue placeholder="Select value" />
                            </SelectTrigger>
                            <SelectContent className="bg-white z-50">
                              {headerValues.map((value, index) => (
                                <SelectItem key={index} value={value}>
                                  {value}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        </div>
                      )}
                      <Input
                        placeholder="Enter table name"
                        value={tableName}
                        onChange={(e) => {
                          setTableName(e.target.value);
                          setSqlNameError(''); // Clear error when input changes
                        }}
                        className={`w-[280px] ${sqlNameError ? 'border-red-500' : ''}`}
                      />
                      <Button 
                        onClick={createMonthlyTable}
                        disabled={!selectedHeader || !tableName || !!monthlyError}
                        className={!isMonthlyTableValid ? "bg-gray-300" : ""}
                      >
                        <Plus className="h-4 w-4 mr-2" />
                        Create Monthly Table
                      </Button>
                    </div>

                    {/* SQL Name Error Alert */}
                    {sqlNameError && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Table Name Error</AlertTitle>
                        <AlertDescription>{sqlNameError}</AlertDescription>
                      </Alert>
                    )}

                    {selectedHeader && (
                      <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-md">
                        <div className="text-sm">
                          <span className="font-medium">{selectedHeader} Value: </span>
                          <span>{headerValue.toFixed(2)}</span>
                        </div>
                        <div className="text-sm">
                          <span className="font-medium">Remaining: </span>
                          <span className={`font-medium ${getRemainingValue() < 0 ? 'text-red-500' : 'text-green-500'}`}>
                            {getRemainingValue().toFixed(2)}
                          </span>
                        </div>
                        {monthlyTable && (
                          <div className="text-sm">
                            <span className="font-medium">Total Allocated: </span>
                            <span className={`font-medium ${monthlyTable.total > headerValue ? 'text-red-500' : 'text-green-500'}`}>
                              {monthlyTable.total.toFixed(2)}
                            </span>
                          </div>
                        )}
                      </div>
                    )}

                    {monthlyError && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>Error</AlertTitle>
                        <AlertDescription>{monthlyError}</AlertDescription>
                      </Alert>
                    )}

                    {monthlyTable && (
                        <div className="space-y-6">
                          <div className="flex justify-end gap-4 mb-4">
                          <button
                              onClick={handleSaveMonthlyTable}
                              disabled={!isMonthlyTableValid || isSaving}
                              className={`px-6 py-1 rounded ${
                                loading 
                                  ? 'bg-gray-400 cursor-not-allowed' 
                                  : 'bg-green-500 hover:bg-green-600'
                              } text-white`}
                            >
                              {isSaving ? 'Saving...' : 'Save to Database'}
                            </button>

                            <Button
                              onClick={() => window.print()}
                              className="flex items-center gap-2 bg-blue-300 hover:bg-blue-600"
                            >
                              <Printer className="h-4 w-4" />
                              Print
                            </Button>
                            <Button
                              onClick={handlePDFExport}
                              className="flex items-center gap-2 bg-red-300 hover:bg-red-600"
                            >
                              <FileText className="h-4 w-4" />
                              Save as PDF
                            </Button>
                          </div>

                          <div>
                            <div className="rounded-md border">
                              <Table>
                                <TableHeader>
                                  <TableRow>
                                    <TableHead>{selectedHeader}</TableHead>
                                    {months.map(month => (
                                      <TableHead key={month}>{month}</TableHead>
                                    ))}
                                    <TableHead>Total</TableHead>
                                  </TableRow>
                                </TableHeader>
                                <TableBody>
                                  <TableRow>
                                    <TableCell>{tableName}</TableCell>
                                    {months.map(month => (
                                      <TableCell key={month}>
                                        <Input
                                          type="number"
                                          value={monthlyData[month] || ''}
                                          onChange={(e) => handleMonthlyValueChange(month, e.target.value)}
                                          className="w-24"
                                        />
                                      </TableCell>
                                    ))}
                                    <TableCell className={getRemainingValue() < 0 ? 'text-red-500' : 'text-green-500'}>
                                      {(headerValue - getRemainingValue()).toFixed(2)}
                                    </TableCell>
                                  </TableRow>
                                </TableBody>
                              </Table>
                            </div>

                            <div className="border rounded-lg p-4">
                              <LineChart width={800} height={400} data={chartData}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Line
                                  type="monotone"
                                  dataKey="value"
                                  stroke="#8884d8"
                                  name={selectedHeader}
                                />
                              </LineChart>
                            </div>
                          </div>
                        </div>
                      )}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
        {/* Footer Section */}
        <div className="w-full bg-gray-800 text-white mt-auto">
          <div className="max-w-7xl mx-auto py-4 px-8 text-center">
            &copy; {new Date().getFullYear()} Dashboard Visualisasi. Dibuat dengan ❤️ oleh Bernardo. All Rights Reserved.
          </div>
        </div>
      </div>
    </>
  );
};

export default TableManager;