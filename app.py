def generate_excel_report():
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # -------------------------
        # Formats
        # -------------------------
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#0D2A3E',
            'font_color': 'white',
            'align': 'center',
            'border': 1
        })

        cell_format = workbook.add_format({
            'border': 1,
            'align': 'center'
        })

        number_2dp = workbook.add_format({
            'border': 1,
            'num_format': '0.00',
            'align': 'center'
        })

        number_4dp = workbook.add_format({
            'border': 1,
            'num_format': '0.0000',
            'align': 'center'
        })

        currency_format = workbook.add_format({
            'border': 1,
            'num_format': '$#,##0.00',
            'align': 'center'
        })

        # -------------------------
        # INPUT SHEET
        # -------------------------
        df_inputs = pd.DataFrame([
            ("Bench Height (m)", inputs_si['bench_height_m']),
            ("Hole Diameter (m)", inputs_si['hole_diameter_m']),
            ("Rock Density (kg/m³)", inputs_si['rock_density_kgpm3']),
            ("Explosive Density (kg/m³)", inputs_si['explosive_density_kgpm3']),
            ("Bench Area (m²)", inputs_si['area_m2']),
            ("Unit Cost ($/t)", inputs_si['unit_cost_per_tonne']),
        ], columns=["Parameter", "Value (SI)"])

        df_inputs.to_excel(writer, sheet_name="Inputs", index=False)
        ws_inputs = writer.sheets["Inputs"]

        # Apply formatting
        ws_inputs.set_column("A:A", 30)
        ws_inputs.set_column("B:B", 25)

        for col_num, value in enumerate(df_inputs.columns):
            ws_inputs.write(0, col_num, value, header_format)

        for row in range(1, len(df_inputs) + 1):
            ws_inputs.write(row, 0, df_inputs.iloc[row-1, 0], cell_format)
            ws_inputs.write(row, 1, df_inputs.iloc[row-1, 1], number_4dp)

        # -------------------------
        # RESULTS SHEET
        # -------------------------
        df_results = pd.DataFrame([
            ("Burden (m)", results_si['burden_m']),
            ("Spacing (m)", results_si['spacing_m']),
            ("Number of Holes", results_si['holes']),
            ("Charge per Hole (t)", results_si['charge_tonnes']),
            ("Total Explosive (t)", results_si['total_exp_tonnes']),
            ("Rock Volume (m³)", results_si['rock_vol_m3']),
            ("Powder Factor (t/m³)", results_si['pf']),
            ("Total Cost ($)", results_si['cost']),
        ], columns=["Parameter", "Value (SI)"])

        df_results.to_excel(writer, sheet_name="Results", index=False)
        ws_results = writer.sheets["Results"]

        ws_results.set_column("A:A", 35)
        ws_results.set_column("B:B", 25)

        for col_num, value in enumerate(df_results.columns):
            ws_results.write(0, col_num, value, header_format)

        for row in range(1, len(df_results) + 1):
            ws_results.write(row, 0, df_results.iloc[row-1, 0], cell_format)

            # Apply specific formatting based on row
            if "Cost" in df_results.iloc[row-1, 0]:
                ws_results.write(row, 1, df_results.iloc[row-1, 1], currency_format)
            elif "Number of Holes" in df_results.iloc[row-1, 0]:
                ws_results.write(row, 1, df_results.iloc[row-1, 1], cell_format)
            elif "Powder Factor" in df_results.iloc[row-1, 0]:
                ws_results.write(row, 1, df_results.iloc[row-1, 1], number_4dp)
            else:
                ws_results.write(row, 1, df_results.iloc[row-1, 1], number_2dp)

        # -------------------------
        # DISPLAY SETTINGS SHEET
        # -------------------------
        df_display = pd.DataFrame([
            ("Length unit", disp['length']),
            ("Area unit", disp['area']),
            ("Density unit", disp['density']),
        ], columns=["Setting", "Unit"])

        df_display.to_excel(writer, sheet_name="Display Units", index=False)
        ws_display = writer.sheets["Display Units"]

        ws_display.set_column("A:A", 25)
        ws_display.set_column("B:B", 20)

        for col_num, value in enumerate(df_display.columns):
            ws_display.write(0, col_num, value, header_format)

        for row in range(1, len(df_display) + 1):
            ws_display.write(row, 0, df_display.iloc[row-1, 0], cell_format)
            ws_display.write(row, 1, df_display.iloc[row-1, 1], cell_format)

    output.seek(0)
    return output
