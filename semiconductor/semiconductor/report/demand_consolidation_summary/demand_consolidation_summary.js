// Copyright (c) 2025, RIT and contributors
// For license information, please see license.txt

frappe.query_reports["Demand Consolidation Summary"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1)
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "region",
            "label": "Region",
            "fieldtype": "Data"
        },
        {
            "fieldname": "demand_type",
            "label": "Demand Type",
            "fieldtype": "Select",
            "options": ["", "Manual", "Sales Forecast", "Market Research", "Historical Sales", "Customer Request", "Consolidated"]
        }
    ]
};
