import React, { useState, useRef, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  Printer, 
  Save, 
  Plus, 
  Trash2, 
  Building, 
  Users, 
  Shield, 
  Gavel, 
  Hammer, 
  Heart, 
  FileText,
  AlertCircle, 
  HelpCircle} from 'lucide-react';
import { Alert, AlertTitle, AlertDescription } from './ui/alert';
import useCustomTablesStore from '../stores/customTablesStore';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable';

/* FinancialDocumentGenerator.jsx */
const customFieldsBySection = {
  PEK: {
    komponen_fisik: [],
  },
  UMPEG: {
    data_kepegawaian: [],
  },
  TRANTIB: {
    sasaran_keamanan: [],
  },
  PEMERINTAHAN: {
    indikator_kinerja: [],
  },
  PEMBANGUNAN: {
    rencana_pembangunan: [],
  },
  KESOS: {
    target_penerima: [],
  },
  PP: {
    pengaduan_masyarakat: [],
  }
};

const FinancialDocumentGenerator = () => {
  const pdfRef = useRef(null);
  const { sectionId } = useParams(); // Ambil sectionId dari URL
  const [documentData, setDocumentData] = useState({
    title: '',
    organization: '',
    fiscalYear: '',
    department: '',
    program: '',
    activity: '',
    subActivity: '',
    fundingSource: '',
    location: '',
    implementationPeriod: '',
    Allocation: '',
    targetGroup: '',
    budget: {
      current: 0,
      next: 0,
      previous: 0
    },
    sectionSpecificFields: {} // Custom fields based on section
  });

  // Custom Header per Section
  const getHeaderBySection = (section) => {
    switch (section) {
      case 'PEK':
        return {
          color: 'bg-blue-600',
          icon: <Building />,
          subtitle: 'Dokumen Perekonomian'
        };
      case 'UMPEG':
        return {
          color: 'bg-indigo-600',
          icon: <Users />,
          subtitle: 'Dokumen Kepegawaian'
        };
      case 'TRANTIB':
        return {
          color: 'bg-red-600',
          icon: <Shield />,
          subtitle: 'Dokumen Ketertiban Umum'
        };
      case 'PEMERINTAHAN':
        return {
          color: 'bg-yellow-600',
          icon: <Gavel />,
          subtitle: 'Dokumen Pemerintahan'
        };
      case 'PEMBANGUNAN':
        return {
          color: 'bg-pink-600',
          icon: <Hammer />,
          subtitle: 'Dokumen Pembangunan'
        };
      case 'KESOS':
        return {
          color: 'bg-purple-600',
          icon: <Heart />,
          subtitle: 'Dokumen Kesejahteraan Sosial'
        };
      case 'PP':
        return {
          color: 'bg-teal-600',
          icon: <FileText />,
          subtitle: 'Dokumen Pemberdayaan Perempuan'
        };
      default:
        return {
          color: 'bg-gray-600',
          icon: <HelpCircle />,
          subtitle: 'Dokumen Tidak Diketahui'
        };
    }
  };

  const getFooterBySection = (section) => {
    switch (section) {
      case 'PEK':
        return {
          color: 'bg-blue-600',
          text: 'Perekonomian'
        };
      case 'UMPEG':
        return {
          color: 'bg-indigo-600',
          text: 'Kepegawaian'
        };
      case 'TRANTIB':
        return {
          color: 'bg-red-600',
          text: 'Ketertiban Umum'
        };
      case 'PEMERINTAHAN':
        return {
          color: 'bg-yellow-600',
          text: 'Pemerintahan'
        };
      case 'PEMBANGUNAN':
        return {
          color: 'bg-pink-600',
          text: 'Pembangunan'
        };
      case 'KESOS':
        return {
          color: 'bg-purple-600',
          text: 'Kesejahteraan Sosial'
        };
      case 'PP':
        return {
          color: 'bg-teal-600',
          text: 'Pemberdayaan Perempuan'
        };
      default:
        return {
          color: 'bg-gray-600',
          text: 'Tidak Diketahui'
        };
    }
  };

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [errors, setErrors] = useState({
    fiscalYear: '',
    Allocation: ''
  });

  const navigate = useNavigate();

  const [budgetError, setBudgetError] = useState(null);

  // convert string to float
  const parseCurrencyString = useCallback((currencyString) => {
    if (!currencyString) return 0;
    return parseFloat(currencyString.replace(/[^0-9.-]+/g, ""));
  }, []);
  
  // State for budget sections
  const [budgetSections, setBudgetSections] = useState([
    {
      id: 1,
      title: "Budget Items",
      items: []
    }
  ]);

  // State for indicators with proper implementation
  const [indicators, setIndicators] = useState([]);

  // Document Data handlers
  const handleDocumentDataChange = (field, value) => {
    // Clear previous error for this field
    setErrors(prev => ({...prev, [field]: ''}));
    
    // Validate Fiscal Year and Allocation
    if (field === 'fiscalYear' || field === 'Allocation') {
      const numValue = Number(value);
      if (isNaN(numValue)) {
        setErrors(prev => ({
          ...prev, 
          [field]: `${field === 'fiscalYear' ? 'Fiscal Year' : 'Allocation'} harus berupa angka`
        }));
        return;
      }
    }
    
    setDocumentData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Indicators handlers
  const addIndicator = () => {
    setIndicators(prev => [...prev, {
      id: Date.now(),
      type: '',
      description: '',
      target: '',
      unit: ''
    }]);
  };

  const updateIndicator = (id, field, value) => {
    setIndicators(prev => prev.map(indicator => 
      indicator.id === id ? { ...indicator, [field]: value } : indicator
    ));
  };

  const removeIndicator = (id) => {
    setIndicators(prev => prev.filter(indicator => indicator.id !== id));
  };

  const {
    customTables,
    addCustomTable,
    updateTableTitle,
    removeCustomTable,
    addHeaderRow,
    addColumn,
    addRow,
    updateHeaderValue,
    removeColumn,
    updateColumn,
    removeHeaderRow,
    updateCellValue,
    removeRow
  } = useCustomTablesStore()

  useEffect(() => {
    if (sectionId) {
      setDocumentData((prev) => ({
        ...prev,
        sectionSpecificFields: customFieldsBySection[sectionId] || {}
      }));
    }
  }, [sectionId]);

  // Budget Section Management
  const addBudgetSection = () => {
    setBudgetSections(prev => [...prev, {
      id: Date.now(),
      title: `Budget Section ${prev.length + 1}`,
      items: []
    }]);
  };

  const updateBudgetSectionTitle = (sectionId, title) => {
    setBudgetSections(prev => prev.map(section =>
      section.id === sectionId ? { ...section, title } : section
    ));
  };

  const addBudgetItem = (sectionId) => {
    setBudgetSections(prev => prev.map(section => {
      if (section.id === sectionId) {
        return {
          ...section,
          items: [...section.items, {
            id: Date.now(),
            code: '',
            description: '',
            quantity: 0,
            unit: '',
            price: 0,
            tax: 0,
            total: 0
          }]
        };
      }
      return section;
    }));
  };

  const updateBudgetItem = (sectionId, itemId, field, value) => {
    setBudgetSections(prev => prev.map(section => {
      if (section.id === sectionId) {
        const newItems = section.items.map(item => {
          if (item.id === itemId) {
            const updatedItem = { ...item, [field]: value };
            if (field === 'quantity' || field === 'price' || field === 'tax') {
              const quantity = field === 'quantity' ? parseFloat(value) : item.quantity;
              const price = field === 'price' ? parseFloat(value) : item.price;
              const tax = field === 'tax' ? parseFloat(value) : item.tax;
              updatedItem.total = quantity * price * (1 + tax/100);
            }
            return updatedItem;
          }
          return item;
        });
        return { ...section, items: newItems };
      }
      return section;
    }));
  };

  const removeBudgetItem = (sectionId, itemId) => {
    setBudgetSections(prev => prev.map(section => {
      if (section.id === sectionId) {
        return {
          ...section,
          items: section.items.filter(item => item.id !== itemId)
        };
      }
      return section;
    }));
  };

  const calculateSectionTotal = useCallback((sectionId) => {
    const section = budgetSections.find(s => s.id === sectionId);
    return section ? section.items.reduce((sum, item) => sum + item.total, 0) : 0;
  }, [budgetSections]);

  const calculateGrandTotal = useCallback(() => {
    return budgetSections.reduce((sum, section) => 
      sum + section.items.reduce((sectionSum, item) => sectionSum + item.total, 0), 0
    );
  }, [budgetSections]);

  const remainingBalance = parseCurrencyString(documentData.Allocation) - calculateGrandTotal();

  const validateBudget = useCallback(() => {
    const fundingAmount = parseCurrencyString(documentData.Allocation);
    const totalBudget = calculateGrandTotal();
    
    if (totalBudget > fundingAmount) {
      setBudgetError(`Total anggaran (${new Intl.NumberFormat('id-ID', { 
        style: 'currency', 
        currency: 'IDR' 
      }).format(totalBudget)}) melebihi sumber dana yang tersedia (${new Intl.NumberFormat('id-ID', { 
        style: 'currency', 
        currency: 'IDR' 
      }).format(fundingAmount)})`);
      
      return {
        isValid: false,
        message: 'Total budget cannot exceed funding source amount'
      };
    } else if (fundingAmount < 0) {
      setBudgetError('Sumber dana tidak boleh negatif');
      return {
        isValid: false,
        message: 'Funding source cannot be negative'
      };
    }
  
    setBudgetError(null);
    return {
      isValid: true,
      message: ''
    };
  }, [documentData.Allocation, calculateGrandTotal, parseCurrencyString]);
  
  // The useEffect remains the same
  useEffect(() => {
    validateBudget();
  }, [validateBudget]);
  

  // Function to format table name (remove spaces, special chars)
  const formatSqlSafeName = (name) => {
    if (!name || name.trim() === '') {
      throw new Error('Table title cannot be empty');
    }

    const formatted = name
      .toLowerCase()
      .replace(/[^a-z0-9_]/g, '_') // Replace non-alphanumeric chars with underscore
      .replace(/^[^a-z]+/, '')     // Remove leading non-letters
      .replace(/_{2,}/g, '_')      // Replace multiple underscores with single
      .replace(/^_|_$/g, '')       // Remove leading/trailing underscores
      .substring(0, 63)            // Ensure name isn't too long for SQL
      || null;                     // Return null if result is empty string

    if (formatted === null) {
      throw new Error(`Invalid table name: "${name}". Table name must contain at least one letter after formatting.`);
    }

    return formatted;
  };

  // Format column header for SQL
  const formatColumnHeader = (header) => {
    const formatted = formatSqlSafeName(header);
    // Ensure it doesn't start with a number
    return /^\d/.test(formatted) ? `col_${formatted}` : formatted;
  };

  const handleSaveToDatabase = async () => {
    setLoading(true);
    setError(null);
  
    try {
      const budgetValidation = validateBudget();
      if (!budgetValidation.isValid) {
        throw new Error(budgetValidation.message);
      }

      // Validate Indicators table title
      if (indicators.length > 0) {
        try {
          formatSqlSafeName("Indikator dan Tolak Ukur Kinerja Kegiatan");
        } catch (error) {
          throw new Error(`Indicators table error: ${error.message}`);
        }
      }

      // Format table and column names
      const formattedTables = customTables.map(table => {
        try {
          const sqlSafeName = formatSqlSafeName(table.title);
          return {
            ...table,
            sqlSafeName,
            headers: table.headers.map(headerRow => ({
              ...headerRow,
              columns: headerRow.columns.map(col => ({
                ...col,
                sqlSafeHeader: formatColumnHeader(col.header)
              }))
            })),
            rows: table.rows.map(row => {
              const rowData = {};
              table.headers[0].columns.forEach(col => {
                rowData[formatColumnHeader(col.header)] = row[col.id] || null;
              });
              return rowData;
            })
          };
        } catch (error) {
          throw new Error(`Custom table "${table.title}" error: ${error.message}`);
        }
      });

      // Validate Budget Sections titles
      budgetSections.forEach(section => {
        try {
          formatSqlSafeName(section.title);
        } catch (error) {
          throw new Error(`Budget section "${section.title}" error: ${error.message}`);
        }
      });

      const payload = {
        customTables: formattedTables,
        budgetSections: budgetSections.map(section => ({
          ...section,
          tableName: formatSqlSafeName(section.title)
        }))
      };

      console.log('Sending payload:', JSON.stringify(payload, null, 2));
  
      const response = await fetch('http://localhost:5000/api/save-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });
  
      if (!response.ok) {
        throw new Error('Failed to save document');
      }
  
      alert('Document saved successfully!');
      
    } catch (error) {
      setError(error.message);
      alert('Failed to save document: ' + error.message);
    } finally {
      setLoading(false);
    }
  };
  
  // PDF Generation
  const generatePDF = () => {
    try {
      const budgetValidation = validateBudget();
      if (!budgetValidation.isValid) {
        alert(budgetValidation.message);
        return;
      }

      const doc = new jsPDF();
      let currentY = 10;
      const pageHeight = doc.internal.pageSize.height;
      const marginBottom = 20;
  
      // Helper function to check and add new page if needed
      const checkAndAddPage = (requiredSpace) => {
        if (currentY + requiredSpace > pageHeight - marginBottom) {
          doc.addPage();
          currentY = 20;
          return true;
        }
        return false;
      };
  
      // Document Title
      doc.setFontSize(16);
      doc.text(documentData.title || 'Financial Document', 5, currentY);
      currentY += 10;
  
      // Create metadata table with two columns
      const metadata = [
        { left: ['Organization'], right: [documentData.organization] },
        { left: ['Fiscal Year'], right: [documentData.fiscalYear] },
        { left: ['Funding Source'], right: [documentData.fundingSource] },
        { left: ['Location'], right: [documentData.location] },
        { left: ['Implementation Period'], right: [documentData.implementationPeriod] },
        { left: ['Target Group'], right: [documentData.targetGroup] },
        { left: ['Department'], right: [documentData.department] },
        { left: ['Program'], right: [documentData.program] },
        { left: ['Activity'], right: [documentData.activity] },
        { left: ['Sub Activity'], right: [documentData.subActivity] },
        { left: ['Allocation Fund'], right: [documentData.Allocation] },
      ];
  
      doc.autoTable({
        startY: currentY,
        head: [],
        body: metadata.map(row => [
          `${row.left[0]} ${row.left[1] || ''}`,
          `${row.right[0]} ${row.right[1] || ''}`
        ]),
        styles: {
          cellPadding: 5,
          fontSize: 10,
          lineColor: [0, 0, 0], // Black borders
          lineWidth: 0.1,
        },
        theme: 'plain',
        headStyles: {
          fillColor: false, // Remove header background
          textColor: [0, 0, 0], // Black text for header
        },
        bodyStyles: {
          fillColor: false, // Remove body background
          textColor: [0, 0, 0], // Black text for body
        },
        alternateRowStyles: {
          fillColor: false // Remove alternate row background
        },
        margin: { left: 10, right: 10 },
      });
  
      currentY = doc.autoTable.previous.finalY + 10;
  
      // Indicators Section
      if (indicators.length > 0) {
        checkAndAddPage(50);
        doc.text('Indicators', 10, currentY);
        currentY += 10;
        
        doc.autoTable({
          startY: currentY,
          head: [
            [{ content: 'Indikator dan Tolak Ukur Kinerja Kegiatan', colSpan: 4, styles: { halign: 'center', fillColor: [240, 240, 240] } }],
            ['Type', 'Description', 'Target', 'Unit']
          ],
          body: indicators.map(indicator => [
            indicator.type || '-',
            indicator.description || '-',
            indicator.target || '-',
            indicator.unit || '-',
          ]),
          styles: {
            cellPadding: 5,
            fontSize: 10,
            lineColor: [0, 0, 0], // Black borders
            lineWidth: 0.1,
          },
          theme: 'plain',
          headStyles: {
            fillColor: false,
            textColor: [0, 0, 0],
            fontStyle: 'normal'
          },
          bodyStyles: {
            fillColor: false,
            textColor: [0, 0, 0]
          },
          alternateRowStyles: {
            fillColor: false
          },
          margin: { top: 10 },
        });
        
        currentY = doc.autoTable.previous.finalY + 10;
      }
  
      // Custom Tables
      customTables.forEach((table) => {
        checkAndAddPage(50);
        doc.text(table.title, 10, currentY);
        currentY += 10;
        doc.autoTable({
          startY: currentY,
          head: [
            [{ content: table.title, colSpan: table.headers[0].columns.length, styles: { halign: 'center', fillColor: [240, 240, 240] } }],
            ...table.headers.map(headerRow => 
              headerRow.columns.map(col => col.header || '-')
            )
          ],
          body: table.rows.map(row =>
            table.headers[0].columns.map(col => row[col.id] || '-')
          ),
          styles: {
            cellPadding: 5,
            fontSize: 10,
            lineColor: [0, 0, 0], // Black borders
            lineWidth: 0.1,
          },
          theme: 'plain',
          headStyles: {
            fillColor: false,
            textColor: [0, 0, 0],
            fontStyle: 'normal'
          },
          bodyStyles: {
            fillColor: false,
            textColor: [0, 0, 0]
          },
          alternateRowStyles: {
            fillColor: false
          },
          margin: { top: 10 },
        });
        currentY = doc.autoTable.previous.finalY + 10;
      });
  
      // Budget Sections
      budgetSections.forEach((section) => {
        checkAndAddPage(50);
        doc.text(section.title, 10, currentY);
        currentY += 10;
  
        doc.autoTable({
          startY: currentY,
          head: [
            [{ content: section.title, colSpan: 7, styles: { halign: 'center', fillColor: [240, 240, 240] } }],
            ['Code', 'Description', 'Quantity', 'Unit', 'Price', 'Tax (%)', 'Total']
          ],
          body: section.items.map(item => [
            item.code || '-',
            item.description || '-',
            item.quantity || 0,
            item.unit || '-',
            new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(item.price || 0),
            item.tax || 0,
            new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR' }).format(item.total || 0),
          ]),
          styles: {
            cellPadding: 5,
            fontSize: 10,
            lineColor: [0, 0, 0], // Black borders
            lineWidth: 0.1,
          },
          theme: 'plain',
          headStyles: {
            fillColor: false,
            textColor: [0, 0, 0],
            fontStyle: 'normal'
          },
          bodyStyles: {
            fillColor: false,
            textColor: [0, 0, 0]
          },
          alternateRowStyles: {
            fillColor: false
          },
          margin: { top: 10 },
        });
  
        currentY = doc.autoTable.previous.finalY + 10;
        
        // Section Total
        checkAndAddPage(15);
        const sectionTotal = calculateSectionTotal(section.id);
        doc.text(
          `Total for ${section.title}: ${new Intl.NumberFormat('id-ID', { 
            style: 'currency', 
            currency: 'IDR' 
          }).format(sectionTotal)}`,
          10,
          currentY
        );
        currentY += 10;
      });
  
      // Grand Total
      checkAndAddPage(15);
      const grandTotal = calculateGrandTotal();
      doc.text(
        `Grand Total: ${new Intl.NumberFormat('id-ID', { 
          style: 'currency', 
          currency: 'IDR' 
        }).format(grandTotal)}`,
        10,
        currentY
      );
      currentY += 10;

      // Sisa Dana
      checkAndAddPage(15);
      const remainingBalance = parseCurrencyString(documentData.Allocation) - calculateGrandTotal();
      doc.text(
        `Sisa Dana: ${new Intl.NumberFormat('id-ID', { 
          style: 'currency', 
          currency: 'IDR' 
        }).format(remainingBalance)}`,
        10,
        currentY
      );
      currentY += 10;
  
      // Approval Section
      const approvalData = {
        name: document.getElementById("approvalName").value,
        position: document.getElementById("approvalPosition").value,
        employeeId: document.getElementById("approvalEmployeeId").value,
        date: document.getElementById("approvalDate").value,
        signature: document.getElementById("approvalSignature").files[0], // File object
      };

      checkAndAddPage(60);
      doc.text('Approval', 10, currentY);
      currentY += 10;

      // Function to handle image loading and get image dimensions
      const getImageData = (file) => {
        return new Promise((resolve) => {
          const reader = new FileReader();
          reader.onload = (e) => {
            const image = new Image();
            image.src = e.target.result;
            image.onload = () => {
              resolve({
                data: e.target.result,
                width: 960,
                height: 960
              });
            };
          };
          reader.readAsDataURL(file);
        });
      };

      // Create table for name, position, employee ID, and date
      doc.autoTable({
        startY: currentY,
        head: [],
        body: [
          ['Name:', approvalData.name],
          ['Position:', approvalData.position],
          ['Employee ID:', approvalData.employeeId],
          ['Date:', approvalData.date]
        ],
        styles: {
          cellPadding: 5,
          fontSize: 10,
        },
        theme: 'grid',
        margin: { left: 10, right: 10 },
        columnStyles: {
          0: { cellWidth: 80 },
          1: { cellWidth: 'auto' },
        }
      });

      currentY = doc.autoTable.previous.finalY + 15;

      // Add "Signature:" text with right alignment
      const pageWidth = doc.internal.pageSize.getWidth();
      doc.setFontSize(10);
      doc.text('Signature:', pageWidth - 10, currentY, { align: 'right' });
      currentY += 10;

      // Modified signature handling
      if (approvalData.signature) {
        getImageData(approvalData.signature).then(imageInfo => {
          const signatureWidth = 960 / 96; 
          const signatureHeight = 960 / 96; 

          // Position signature on the right side
          const pageWidth = doc.internal.pageSize.getWidth();
          doc.addImage(
            imageInfo.data,
            'PNG',
            pageWidth - signatureWidth - 10, // Position from right margin
            currentY,
            signatureWidth,
            signatureHeight
          );

          // Save PDF after image is added
          const fileName = documentData.title ? `${documentData.title}.pdf` : 'FinancialDocument.pdf';
          doc.save(fileName);
        });
      } else {
        // Save PDF if no signature
        const fileName = documentData.title ? `${documentData.title}.pdf` : 'FinancialDocument.pdf';
        doc.save(fileName);
      }
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Failed to generate PDF. Please check console for details.');
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

  return (
    <>
      <style>{printStyles}</style>
      <div className="max-w-7xl mx-auto p-6 space-y-8" ref={pdfRef}>
        {/* Header Controls */}
        <div className={`${getHeaderBySection(sectionId).color} flex justify-between items-center`}>
          {getHeaderBySection(sectionId).icon}
          <div className="flex flex-col items-center">
            <h1 className="text-2xl font-bold">Financial Document Generator</h1>
            <h2 className="text-2xl font-bold">{getHeaderBySection(sectionId).subtitle}</h2>
          </div>

          <div className="space-x-4">
            <button
              onClick={handleSaveToDatabase}
              disabled={loading}
              className={`px-6 py-1 rounded ${
                loading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-green-500 hover:bg-green-600'
              } text-white`}
            >
              {loading ? 'Saving...' : 'Save to Database'}
            </button>
            
            {error && (
              <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
                {error}
              </div>
            )}
            <button
              onClick={generatePDF}
              className="px-4 py-1 bg-gray-600 text-white rounded-md flex items-center gap-2"
            >
              <Save size={20} />
              Save as PDF
            </button>
            <button
              onClick={() => window.print()}
              className="px-4 py-1 bg-lime-600 text-white rounded-md flex items-center gap-2"
            >
              <Printer size={20} />
              Print
            </button>
            <button
              onClick={() => navigate('/table-manager')}
              className="px-4 py-1 bg-cyan-600 text-white rounded-md flex items-center gap-2"
            >
              RAK
            </button>
          </div>
        </div>

        {/* Document Header */}
        <div className="grid grid-cols-2 gap-6 bg-white p-6 rounded-lg shadow page-break-after">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Document Title</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.title}
                onChange={(e) => handleDocumentDataChange('title', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Organization</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.organization}
                onChange={(e) => handleDocumentDataChange('organization', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Fiscal Year</label>
              <input
                type="text"
                className={`mt-1 block w-full rounded-md ${
                  errors.fiscalYear ? 'border-red-500' : 'border-gray-300'
                } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                value={documentData.fiscalYear}
                onChange={(e) => handleDocumentDataChange('fiscalYear', e.target.value)}
              />
              {errors.fiscalYear && (
                <p className="mt-1 text-sm text-red-600">{errors.fiscalYear}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Funding Source</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.fundingSource}
                onChange={(e) => handleDocumentDataChange('fundingSource', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Location</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.location}
                onChange={(e) => handleDocumentDataChange('location', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Implementation Period</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.implementationPeriod}
                onChange={(e) => handleDocumentDataChange('implementationPeriod', e.target.value)}
              />
            </div>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Department</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.department}
                onChange={(e) => handleDocumentDataChange('department', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Program</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.program}
                onChange={(e) => handleDocumentDataChange('program', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Activity</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.activity}
                onChange={(e) => handleDocumentDataChange('activity', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Sub Activity</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.subActivity}
                onChange={(e) => handleDocumentDataChange('subActivity', e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Allocation</label>
              <input
                type="text"
                className={`mt-1 block w-full rounded-md ${
                  errors.Allocation ? 'border-red-500' : 'border-gray-300'
                } shadow-sm focus:border-blue-500 focus:ring-blue-500`}
                value={documentData.Allocation}
                onChange={(e) => handleDocumentDataChange('Allocation', e.target.value)}
              />
              {errors.Allocation && (
                <p className="mt-1 text-sm text-red-600">{errors.Allocation}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Target Group</label>
              <input
                type="text"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                value={documentData.targetGroup}
                onChange={(e) => handleDocumentDataChange('targetGroup', e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* Indicators Section */}
        <div className="bg-white p-6 rounded-lg shadow page-break-after">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Performance Indicators</h2>
            <button
              onClick={addIndicator}
              className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2"
            >
              <Plus size={20} />
              Add Indicator
            </button>
          </div>
          <div className="space-y-4">
            {indicators.map((indicator) => (
              <div key={indicator.id} className="grid grid-cols-12 gap-4 items-start">
                <div className="col-span-3">
                  <select
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={indicator.type}
                    onChange={(e) => updateIndicator(indicator.id, 'type', e.target.value)}
                  >
                    <option value="">Select Type</option>
                    <option value="program">Program</option>
                    <option value="input">Input</option>
                    <option value="output">Output</option>
                    <option value="outcome">Outcome</option>
                  </select>
                </div>
                <div className="col-span-5">
                  <input
                    type="text"
                    placeholder="Description"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={indicator.description}
                    onChange={(e) => updateIndicator(indicator.id, 'description', e.target.value)}
                  />
                </div>
                <div className="col-span-2">
                  <input
                    type="text"
                    placeholder="Target"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={indicator.target}
                    onChange={(e) => updateIndicator(indicator.id, 'target', e.target.value)}
                  />
                </div>
                <div className="col-span-1">
                  <input
                    type="text"
                    placeholder="Unit"
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    value={indicator.unit}
                    onChange={(e) => updateIndicator(indicator.id, 'unit', e.target.value)}
                  />
                </div>
                <div className="col-span-1">
                  <button
                    onClick={() => removeIndicator(indicator.id)}
                    className="mt-1 p-2 text-red-600 hover:text-red-800"
                  >
                    <Trash2 size={20} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Custom Tables Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Custom Tables</h2>
            <div className="flex gap-2">
              <button
                onClick={() => addCustomTable(sectionId)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2"
              >
                <Plus size={20} />
                Add {sectionId} Template
              </button>
            </div>
          </div>

          <div className="space-y-4">
            {customTables.map(table => (
              <div key={table.id} className="mb-8 border p-4 rounded-lg">
                <div className="flex justify-between items-center mb-4">
                  <input
                    type="text"
                    value={table.title}
                    onChange={(e) => updateTableTitle(table.id, e.target.value)}
                    className="text-lg font-semibold bg-transparent border-b border-gray-300 focus:border-blue-500 focus:ring-0"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => removeCustomTable(table.id)}
                      className="px-3 py-1 bg-red-600 text-white rounded-md flex items-center gap-1 text-sm"
                    >
                      <Trash2 size={16} />
                      Remove Table
                    </button>
                    <button
                      onClick={() => addHeaderRow(table.id)}
                      className="px-3 py-1 bg-blue-600 text-white rounded-md flex items-center gap-1 text-sm"
                    >
                      <Plus size={16} />
                      Add Header Row
                    </button>
                    <button
                      onClick={() => addColumn(table.id)}
                      className="px-3 py-1 bg-green-600 text-white rounded-md flex items-center gap-1 text-sm"
                    >
                      <Plus size={16} />
                      Add Column
                    </button>
                    <button
                      onClick={() => addRow(table.id)}
                      className="px-3 py-1 bg-pink-600 text-white rounded-md flex items-center gap-1 text-sm"
                    >
                      <Plus size={16} />
                      Add Row
                    </button>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full border-collapse">
                    <thead>
                      <tr>
                        <th colSpan={table.headers[0].columns.length} className="p-2 border text-center">
                          {table.title}
                        </th>
                      </tr>
                      {table.headers.map((headerRow, rowIndex) => (
                        <tr key={headerRow.id}>
                          {headerRow.columns.map((column, colIndex) => (
                            <th key={column.id} className="p-2 border">
                              <div className="flex flex-col gap-2">
                                <div className="flex justify-between items-center">
                                  <input
                                    type="text"
                                    value={column.header}
                                    onChange={(e) => updateHeaderValue(table.id, headerRow.id, column.id, e.target.value)}
                                    className="w-full bg-transparent"
                                    placeholder={rowIndex === 0 ? `Column ${colIndex + 1}` : ''}
                                  />
                                  {rowIndex === 0 && (
                                    <button
                                      onClick={() => removeColumn(table.id, colIndex)}
                                      className="ml-2 text-red-600 hover:text-red-800"
                                      title="Remove Column"
                                    >
                                      <Trash2 size={16} />
                                    </button>
                                  )}
                                </div>
                                {rowIndex === 0 && (
                                  <select
                                    value={column.type}
                                    onChange={(e) => updateColumn(table.id, column.id, 'type', e.target.value)}
                                    className="w-full mt-1 text-sm"
                                  >
                                    <option value="text">Text</option>
                                    <option value="number">Number</option>
                                    <option value="date">Date</option>
                                  </select>
                                )}
                              </div>
                            </th>
                          ))}
                          <th className="w-10 p-2">
                            {rowIndex > 0 && (
                              <button
                                onClick={() => removeHeaderRow(table.id, headerRow.id)}
                                className="text-red-600 hover:text-red-800"
                              >
                                <Trash2 size={16} />
                              </button>
                            )}
                          </th>
                        </tr>
                      ))}
                    </thead>
                    <tbody>
                      {table.rows.map((row, rowIndex) => (
                        <tr key={row.id}>
                          {table.headers[0].columns.map(column => (
                            <td key={column.id} className="p-2 border">
                              <input
                                type={column.type}
                                value={row[column.id] || ''}
                                onChange={(e) => updateCellValue(table.id, rowIndex, column.id, e.target.value)}
                                className="w-full bg-transparent"
                              />
                            </td>
                          ))}
                          <td className="w-10 p-2">
                            <button
                              onClick={() => removeRow(table.id, rowIndex)}
                              className="text-red-600 hover:text-red-800"
                              title="Remove Row"
                            >
                              <Trash2 size={16} />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        </div>

        {budgetError && (
          <Alert variant="destructive" className="mt-4 mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error Anggaran</AlertTitle>
            <AlertDescription>{budgetError}</AlertDescription>
          </Alert>
        )}

        {/* Budget Sections */}
        <div className="space-y-6">
          {budgetSections.map(section => (
            <div key={section.id} className="bg-white p-6 rounded-lg shadow page-break-inside-avoid">
              <div className="flex justify-between items-center mb-4">
                <input
                  type="text"
                  value={section.title}
                  onChange={(e) => updateBudgetSectionTitle(section.id, e.target.value)}
                  className="text-xl font-semibold bg-transparent border-b border-gray-300 focus:border-blue-500 focus:ring-0"
                />
                <button
                  onClick={() => addBudgetItem(section.id)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2"
                >
                  <Plus size={20} />
                  Add Item
                </button>
              </div>

              <div className="space-y-4">
                {section.items.map((item) => (
                  <div key={item.id} className="grid grid-cols-12 gap-4 items-start">
                    <div className="col-span-2">
                      <input
                        type="text"
                        placeholder="Code"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.code}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'code', e.target.value)}
                      />
                    </div>
                    <div className="col-span-3">
                      <input
                        type="text"
                        placeholder="Description"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.description}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'description', e.target.value)}
                      />
                    </div>
                    <div className="col-span-1">
                      <input
                        type="number"
                        placeholder="Qty"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.quantity}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'quantity', e.target.value)}
                      />
                    </div>
                    <div className="col-span-1">
                      <input
                        type="text"
                        placeholder="Unit"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.unit}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'unit', e.target.value)}
                      />
                    </div>
                    <div className="col-span-2">
                      <input
                        type="number"
                        placeholder="Price"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.price}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'price', e.target.value)}
                      />
                    </div>
                    <div className="col-span-1">
                      <input
                        type="number"
                        placeholder="Tax %"
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                        value={item.tax}
                        onChange={(e) => updateBudgetItem(section.id, item.id, 'tax', e.target.value)}
                      />
                    </div>
                    <div className="col-span-1">
                      <div className="mt-1 block w-full p-2 bg-gray-50 rounded-md">
                        {new Intl.NumberFormat('id-ID', {
                          style: 'currency',
                          currency: 'IDR'
                        }).format(item.total)}
                      </div>
                    </div>
                    <div className="col-span-1">
                      <button
                        onClick={() => removeBudgetItem(section.id, item.id)}
                        className="mt-1 pl-10 p-2 text-red-600 hover:text-red-800"
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-6 text-right text-xl font-bold">
                Section Total: {new Intl.NumberFormat('id-ID', {
                  style: 'currency',
                  currency: 'IDR'
                }).format(calculateSectionTotal(section.id))}
              </div>
            </div>
          ))}

          <div className="flex justify-between items-center">
            <button
              onClick={addBudgetSection}
              className="px-4 py-2 bg-blue-600 text-white rounded-md flex items-center gap-2"
            >
              <Plus size={20} />
              Add Budget Section
            </button>
            <div className="text-2xl font-bold">
              Grand Total: {new Intl.NumberFormat('id-ID', {
                style: 'currency',
                currency: 'IDR'
              }).format(calculateGrandTotal())}
            </div>
            <div className={`text-2xl font-bold ${remainingBalance < 0 ? 'text-red-600' : ''}`}>
              Sisa Dana: {new Intl.NumberFormat('id-ID', { 
                style: 'currency', 
                currency: 'IDR' 
              }).format(remainingBalance)}
            </div>
          </div>
        </div>

        {/* Signature Section */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Approval</h2>
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  id="approvalName"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Position</label>
                <input
                  type="text"
                  id="approvalPosition"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Employee ID</label>
                <input
                  type="text"
                  id="approvalEmployeeId"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Date</label>
                <input
                  type="date"
                  id="approvalDate"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Signature</label>
                <input
                  type="file"
                  id="approvalSignature"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  accept="image/*"
                />
              </div>
            </div>
          </div>
        </div>
        <div className={`${getFooterBySection(sectionId).color} flex justify-center items-center p-4`}>
          <p className="text-2xl font-bold">{getFooterBySection(sectionId).text}</p>
        </div>
      </div>
    </>
  );
};

export default FinancialDocumentGenerator;