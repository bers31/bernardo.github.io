const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function saveToDatabase(customTables, budgetSections) {
  try {
    return await prisma.$transaction(async (tx) => {
      // Save custom tables
      const savedCustomTables = await Promise.all(
        customTables.map(async (table) => {
          // Escape table name
          const tableName = `\`${table.sqlSafeName}\``;
          
          // Build column definitions
          const columnDefs = table.headers[0].columns.map(col => {
            const colName = `\`${col.sqlSafeHeader}\``;
            const colType = getColumnType(col.type);
            return `${colName} ${colType}`;
          }).join(',\n              ');

          // Create table query
          const createTableQuery = `
            CREATE TABLE IF NOT EXISTS ${tableName} (
              \`id\` INT NOT NULL AUTO_INCREMENT,
              ${columnDefs},
              PRIMARY KEY (\`id\`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
          `;
          
          console.log('Creating table with query:', createTableQuery); // Debug log
          
          await tx.$executeRawUnsafe(createTableQuery);

          // Create metadata entry
          const tableMetadata = await tx.tableMetadata.create({
            data: {
              tableName: table.sqlSafeName,
              title: table.title,
              columns: table.headers[0].columns.map(col => ({
                name: col.sqlSafeHeader,
                type: col.type,
                header: col.header
              }))
            }
          });

          // In the customTables mapping section:
          if (table.rows.length > 0) {
            const columns = table.headers[0].columns.map(col => `\`${col.sqlSafeHeader}\``);
            const values = table.rows.map(row => {
              return table.headers[0].columns.map(col => {
                const value = row[col.sqlSafeHeader];
                return value !== undefined ? value : null;
              });
            });

            const placeholders = values.map(() => 
              `(${columns.map(() => '?').join(',')})`
            ).join(',');

            const insertQuery = `
              INSERT INTO ${tableName} (${columns.join(',')})
              VALUES ${placeholders};
            `;
            
            console.log('Inserting data with query:', insertQuery); // Debug log
            console.log('Values:', values.flat()); // Debug log
            
            const flatValues = values.flat();
            await tx.$executeRawUnsafe(insertQuery, ...flatValues);
          }

          return tableMetadata;
        })
      );

      // Save budget sections
      const savedBudgetSections = await Promise.all(
        budgetSections.map(async (section) => {
          const sectionTableName = `\`${formatTableName(section.title)}\``;
          
          const createSectionQuery = `
            CREATE TABLE IF NOT EXISTS ${sectionTableName} (
              \`id\` INT NOT NULL AUTO_INCREMENT,
              \`code\` VARCHAR(255),
              \`description\` TEXT,
              \`quantity\` DECIMAL(10,2),
              \`unit\` VARCHAR(50),
              \`price\` DECIMAL(10,2),
              \`tax\` DECIMAL(10,2),
              \`total\` DECIMAL(10,2),
              PRIMARY KEY (\`id\`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
          `;
          
          console.log('Creating budget section table with query:', createSectionQuery); // Debug log

          await tx.$executeRawUnsafe(createSectionQuery);

          const sectionMetadata = await tx.budgetSectionMetadata.create({
            data: {
              tableName: section.tableName || formatTableName(section.title),
              title: section.title,
              totalAmount: calculateSectionTotal(section)
            }
          });

          if (section.items.length > 0) {
            const items = section.items.map(item => [
              item.code,
              item.description,
              item.quantity,
              item.unit,
              item.price,
              item.tax,
              item.total
            ]);

            const placeholders = items.map(() => 
              '(?,?,?,?,?,?,?)'
            ).join(',');

            const insertQuery = `
              INSERT INTO ${sectionTableName} 
              (\`code\`, \`description\`, \`quantity\`, \`unit\`, \`price\`, \`tax\`, \`total\`)
              VALUES ${placeholders};
            `;
            
            console.log('Inserting budget items with query:', insertQuery); // Debug log

            await tx.$executeRawUnsafe(insertQuery, ...items.flat());
          }

          return sectionMetadata;
        })
      );

      return {
        customTables: savedCustomTables,
        budgetSections: savedBudgetSections
      };
    });

  } catch (error) {
    console.error('Database save error:', error);
    console.error('Error details:', error.meta); // Additional error details
    throw new Error(`Failed to save tables: ${error.message}`);
  }
}

function getColumnType(type) {
  switch (type?.toLowerCase()) {
    case 'number':
      return 'DECIMAL(10,2)';
    case 'date':
      return 'DATE';
    case 'integer':
      return 'INT';
    case 'boolean':
      return 'BOOLEAN';
    default:
      return 'VARCHAR(255)';
  }
}

function formatTableName(name) {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9_]/g, '_')
    .replace(/^[^a-z]+/, '')
    .replace(/_{2,}/g, '_')
    .replace(/^_|_$/g, '')
    .substring(0, 63)
    || 'unnamed_table';
}

function calculateSectionTotal(section) {
  return section.items.reduce((sum, item) => sum + (parseFloat(item.total) || 0), 0);
}

async function saveMonthlyTable(monthlyTableData) {
  try {
    return await prisma.$transaction(async (tx) => {
      const { customTables } = monthlyTableData;
      
      const savedTables = await Promise.all(
        customTables.map(async (table) => {
          // 1. Buat tabel fisik di database
          const tableName = `\`${table.sqlSafeName}\``;
          const createTableQuery = `
            CREATE TABLE IF NOT EXISTS ${tableName} (
              \`id\` INT NOT NULL AUTO_INCREMENT,
              \`month\` VARCHAR(255) NOT NULL,
              \`${table.headers[1].sqlSafeName}\` DECIMAL(10,2) NOT NULL,
              PRIMARY KEY (\`id\`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
          `;
          
          await tx.$executeRawUnsafe(createTableQuery);

          // 2. Simpan metadata tabel
          const monthMetadata = await tx.monthMetadata.create({
            data: {
              tableName: table.sqlSafeName,
              title: table.title,
              headers: table.headers.map(header => header.name) // Menyimpan informasi header asli
            }
          });

          // 3. Insert data bulanan
          if (table.rows && table.rows.length > 0) {
            const insertQuery = `
              INSERT INTO ${tableName} (month, \`${table.headers[1].sqlSafeName}\`)
              VALUES ${table.rows.map(() => '(?, ?)').join(',')};
            `;
            
            const values = table.rows.flatMap(row => [
              row.month,
              row[table.headers[1].sqlSafeName]
            ]);

            await tx.$executeRawUnsafe(insertQuery, ...values);
          }

          return monthMetadata;
        })
      );

      return {
        customTables: savedTables
      };
    });
  } catch (error) {
    console.error('Monthly table save error:', error);
    throw new Error(`Failed to save monthly table: ${error.message}`);
  }
}

module.exports = { saveToDatabase, saveMonthlyTable };