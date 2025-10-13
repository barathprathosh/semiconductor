# Copyright (c) 2025, RIT and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}

    # Build dynamic SQL conditions based on filters
    conditions = "1=1"
    values = {}

    if filters.get("region"):
        conditions += " AND so.custom_region = %(region)s"
        values["region"] = filters.get("region")

    if filters.get("demand_type"):
        conditions += " AND so.custom_demand_type = %(demand_type)s"
        values["demand_type"] = filters.get("demand_type")

    if filters.get("from_date"):
        conditions += " AND so.transaction_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")

    if filters.get("to_date"):
        conditions += " AND so.transaction_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")

    columns = [
        {"label": "Item Code", "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 200},
        {"label": "Demand Type", "fieldname": "custom_demand_type", "fieldtype": "Data", "width": 150},
        {"label": "Region", "fieldname": "custom_region", "fieldtype": "Data", "width": 120},
        {"label": "Total Quantity", "fieldname": "total_qty", "fieldtype": "Float", "width": 120},
        {"label": "Avg Rate", "fieldname": "avg_rate", "fieldtype": "Currency", "width": 100},
        {"label": "No. of Orders", "fieldname": "count_orders", "fieldtype": "Int", "width": 100},
    ]

    query = f"""
        SELECT
            soi.item_code,
            so.custom_demand_type,
            so.custom_region,
            SUM(soi.qty) AS total_qty,
            AVG(soi.rate) AS avg_rate,
            COUNT(DISTINCT so.name) AS count_orders
        FROM
            `tabSales Order` so
        JOIN
            `tabSales Order Item` soi ON soi.parent = so.name
        WHERE
            {conditions} AND so.docstatus < 2
        GROUP BY
            soi.item_code, so.custom_demand_type, so.custom_region
        ORDER BY
            soi.item_code, so.custom_demand_type
    """

    data = frappe.db.sql(query, values, as_dict=True)
    return columns, data

