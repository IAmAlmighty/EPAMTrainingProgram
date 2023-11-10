"""Assuming this data is a copy of Schema Mapping document."""


class PersonAddress:
    schema_name = "Person"
    table_name = "Address"
    schema_details = [('Person', 'Address', 'AddressID', 1, None, 'NO', 'int', None),
                      ('Person', 'Address', 'AddressLine1', 2, None, 'NO', 'nvarchar', 60),
                      ('Person', 'Address', 'AddressLine2', 3, None, 'YES', 'nvarchar', 60),
                      ('Person', 'Address', 'City', 4, None, 'NO', 'nvarchar', 30),
                      ('Person', 'Address', 'StateProvinceID', 5, None, 'NO', 'int', None),
                      ('Person', 'Address', 'PostalCode', 6, None, 'NO', 'nvarchar', 15),
                      ('Person', 'Address', 'SpatialLocation', 7, None, 'YES', 'geography', -1),
                      ('Person', 'Address', 'rowguid', 8, '(newid())', 'NO', 'uniqueidentifier', None),
                      ('Person', 'Address', 'ModifiedDate', 9, '(getdate())', 'NO', 'datetime', None)]


class ProductionDocument:
    schema_name = "Production"
    table_name = "Document"
    schema_details = [('Production', 'Document', 'DocumentNode', 1, None, 'NO', 'hierarchyid', 892),
                      ('Production', 'Document', 'DocumentLevel', 2, None, 'YES', 'smallint', None),
                      ('Production', 'Document', 'Title', 3, None, 'NO', 'nvarchar', 50),
                      ('Production', 'Document', 'Owner', 4, None, 'NO', 'int', None),
                      ('Production', 'Document', 'FolderFlag', 5, '((0))', 'NO', 'bit', None),
                      ('Production', 'Document', 'FileName', 6, None, 'NO', 'nvarchar', 400),
                      ('Production', 'Document', 'FileExtension', 7, None, 'NO', 'nvarchar', 8),
                      ('Production', 'Document', 'Revision', 8, None, 'NO', 'nchar', 5),
                      ('Production', 'Document', 'ChangeNumber', 9, '((0))', 'NO', 'int', None),
                      ('Production', 'Document', 'Status', 10, None, 'NO', 'tinyint', None),
                      ('Production', 'Document', 'DocumentSummary', 11, None, 'YES', 'nvarchar', -1),
                      ('Production', 'Document', 'Document', 12, None, 'YES', 'varbinary', -1),
                      ('Production', 'Document', 'rowguid', 13, '(newid())', 'NO', 'uniqueidentifier', None),
                      ('Production', 'Document', 'ModifiedDate', 14, '(getdate())', 'NO', 'datetime', None)]


class ProductionUnitMeasure:
    schema_name = "Production"
    table_name = "UnitMeasure"
    schema_details = [('Production', 'UnitMeasure', 'UnitMeasureCode', 1, None, 'NO', 'nchar', 3),
                      ('Production', 'UnitMeasure', 'Name', 2, None, 'NO', 'nvarchar', 50),
                      ('Production', 'UnitMeasure', 'ModifiedDate', 3, '(getdate())', 'NO', 'datetime', None)]


TABLES = {PersonAddress.__name__: PersonAddress,
          ProductionDocument.__name__: ProductionDocument,
          ProductionUnitMeasure.__name__: ProductionUnitMeasure,
          }
AGG_SCHEMAS_TABLES_NAMES = [(table.schema_name, table.table_name) for table in TABLES.values() if
                            table.table_name != ProductionUnitMeasure.table_name]
