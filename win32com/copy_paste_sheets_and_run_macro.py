import win32com.client as win32

excel = win32.DispatchEx("Excel.Application")

excel.DisplayAlerts = False
excel.Visible = True

wb_source = excel.Workbooks.Open(r"C:\Users\test\Downloads\CT\ABCD.xlsx")
ws_source = wb_source.Worksheets("ABCD")
sourceRow = ws_source.UsedRange.Rows.Count

wb_destination = excel.Workbooks.Open(r"C:\Users\test\Downloads\C_T\CycleTime_Device_Tool.xlsm")
ws_destination_cData = wb_destination.Worksheets("C_data")

# Copy and paste
ws_source.Range("A1:AF"+str(sourceRow)).Copy(ws_destination_cData.Range("A1:AF"+str(sourceRow)))

# Run macro named 'sorting'
excel.Application.Run("sorting")
ws_destination_summary = wb_destination.Worksheets("Summary")
summaryRow = ws_destination_summary.UsedRange.Rows.Count

wb_final_destination = excel.Workbooks.Open(r"C:\Users\test\Downloads\C_T\CT_Summary_CycleTime.xlsx")
new_sheet = wb_final_destination.Sheets.Add(After=wb_final_destination.Sheets(wb_final_destination.Sheets.Count))
new_sheet.Name = "Data_CABGA"

# Copy and paste
ws_destination_summary.Range("A1:AF"+str(summaryRow)).Copy(new_sheet.Range("A1:AF"+str(summaryRow)))

wb_destination.Save()
wb_destination.Close()
wb_source.Close()
wb_final_destination.Save()
wb_final_destination.Close()

excel.Application.Quit()
