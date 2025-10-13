import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_demand_custom_fields():
    custom_fields = {
        "Sales Order": [
            dict(
                fieldname="custom_justification",
                label="Justification",
                fieldtype="Small Text",
                insert_after="order_type",
                reqd=0,
                description="Business justification for demand request"
            ),
            dict(
                fieldname="custom_priority",
                label="Priority",
                fieldtype="Select",
                options="\nHigh\nMedium\nLow",
                insert_after="custom_justification",
                reqd=0,
                description="Demand priority level"
            ),
            dict(
                fieldname="custom_region",
                label="Region",
                fieldtype="Data",
                insert_after="custom_priority",
                reqd=0,
                description="Geographic location or market"
            ),
            dict(
                fieldname="custom_demand_type",
                label="Demand Type",
                fieldtype="Select",
                options="\nManual\nSales Forecast\nMarket Research\nHistorical Sales\nCustomer Request\nConsolidated",
                insert_after="custom_region",
                reqd=0,
                description="Source of demand data"
            ),
            dict(
                fieldname="custom_source_ref",
                label="Source Reference",
                fieldtype="Data",
                insert_after="custom_demand_type",
                reqd=0,
                description="Reference IDs of linked demand sources"
            )
        ]
    }

    create_custom_fields(custom_fields)
    frappe.db.commit()
    frappe.msgprint("✅ Demand Management custom fields added to Sales Order!")


import frappe
from frappe.utils import add_days, nowdate
import random

def create_demo_demand_sales_orders():
    customers = [
        "Riverstone Infotech Pvt. Ltd.",
        "GlobalTech Pvt. Ltd.",
        "Fusion Electronics Ltd.",
        "NextWave Components",
        "Prime Circuits Pvt. Ltd."
    ]

    items = [
        {"item_code": "CPU-AMD-RYZEN7-7840HS", "description": "AMD Ryzen 7 7840HS Laptop CPU"},
        {"item_code": "CPU-QC-SNAPDRAGON-8GEN3", "description": "Qualcomm Snapdragon 8 Gen 3 Mobile CPU"},
        {"item_code": "GPU-NVIDIA-RTX4070", "description": "NVIDIA RTX 4070 GPU"},
        {"item_code": "RAM-32GB-DDR5", "description": "32GB DDR5 RAM Module"},
        {"item_code": "SSD-1TB-NVME", "description": "1TB NVMe SSD"}
    ]

    priorities = ["High", "Medium", "Low"]
    regions = ["India", "United States", "Europe", "Japan"]
    justifications = [
        "Bulk demand for Q4 production ramp-up",
        "Market forecast indicates sales increase",
        "Customer backlog clearance",
        "New OEM partnership commitments",
        "Urgent requirement due to supply chain delay"
    ]
    demand_types = [
        "Manual",
        "Sales Forecast",
        "Market Research",
        "Historical Sales",
        "Customer Request"
    ]

    created_orders = []

    # Create base demand (individual)
    for i in range(25):
        customer = random.choice(customers)
        item = random.choice(items)
        qty = random.randint(50, 400)
        delivery_date = add_days(nowdate(), random.randint(10, 60))

        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": customer,
            "transaction_date": nowdate(),
            "delivery_date": delivery_date,
            "company": "Riverstone Infotech Pvt. Ltd.",
            "custom_justification": random.choice(justifications),
            "custom_priority": random.choice(priorities),
            "custom_region": random.choice(regions),
            "custom_demand_type": random.choice(demand_types),
            "items": [
                {
                    "item_code": item["item_code"],
                    "qty": qty,
                    "rate": random.randint(100, 500),
                    "description": item["description"]
                }
            ]
        })

        so.insert(ignore_permissions=True)
        frappe.db.commit()
        created_orders.append(so.name)

    # Consolidated Demand (aggregated view)
    for item in items:
        total_qty = random.randint(500, 1500)
        so = frappe.get_doc({
            "doctype": "Sales Order",
            "customer": "Riverstone Infotech Pvt. Ltd.",
            "transaction_date": nowdate(),
            "delivery_date": add_days(nowdate(), 45),
            "company": "Riverstone Infotech Pvt. Ltd.",
            "custom_justification": "Aggregated demand from multiple sources (auto-generated)",
            "custom_priority": "High",
            "custom_region": "Global",
            "custom_demand_type": "Consolidated",
            "custom_source_ref": ", ".join(random.sample(created_orders, 3)),
            "items": [
                {
                    "item_code": item["item_code"],
                    "qty": total_qty,
                    "rate": random.randint(100, 500),
                    "description": item["description"]
                }
            ]
        })

        so.insert(ignore_permissions=True)
        frappe.db.commit()

    frappe.msgprint("✅ Demo Demand Data Created: 25 Source + 5 Consolidated Orders")


import frappe

def create_demo_items():
    items = [
        {"item_code": "CPU-AMD-RYZEN7-7840HS", "item_name": "AMD Ryzen 7 7840HS Laptop CPU", "item_group": "Products", "stock_uom": "Nos", "description": "Laptop CPU for high-end laptops"},
        {"item_code": "CPU-QC-SNAPDRAGON-8GEN3", "item_name": "Qualcomm Snapdragon 8 Gen 3 Mobile CPU", "item_group": "Products", "stock_uom": "Nos", "description": "Mobile CPU for flagship smartphones"},
        {"item_code": "GPU-NVIDIA-RTX4070", "item_name": "NVIDIA RTX 4070 GPU", "item_group": "Products", "stock_uom": "Nos", "description": "High-performance GPU for gaming laptops"},
        {"item_code": "RAM-32GB-DDR5", "item_name": "32GB DDR5 RAM Module", "item_group": "Products", "stock_uom": "Nos", "description": "High-speed RAM module for desktops/laptops"},
        {"item_code": "SSD-1TB-NVME", "item_name": "1TB NVMe SSD", "item_group": "Products", "stock_uom": "Nos", "description": "Fast storage SSD for high-performance systems"}
    ]

    for itm in items:
        if not frappe.db.exists("Item", itm["item_code"]):
            item_doc = frappe.get_doc({
                "doctype": "Item",
                "item_code": itm["item_code"],
                "item_name": itm["item_name"],
                "item_group": itm["item_group"],
                "stock_uom": itm["stock_uom"],
                "description": itm["description"]
            })
            item_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"✅ Item created: {itm['item_code']}")
        else:
            print(f"⚠ Item already exists: {itm['item_code']}")


def create_demo_customers():
    customers = [
        {"customer_name": "Riverstone Infotech Pvt. Ltd.", "customer_group": "Commercial", "territory": "India"},
        {"customer_name": "GlobalTech Pvt. Ltd.", "customer_group": "Commercial", "territory": "United States"},
        {"customer_name": "Fusion Electronics Ltd.", "customer_group": "Commercial", "territory": "Europe"},
        {"customer_name": "NextWave Components", "customer_group": "Commercial", "territory": "Japan"},
        {"customer_name": "Prime Circuits Pvt. Ltd.", "customer_group": "Commercial", "territory": "India"}
    ]

    for cust in customers:
        if not frappe.db.exists("Customer", cust["customer_name"]):
            cust_doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": cust["customer_name"],
                "customer_group": cust["customer_group"],
                "territory": cust["territory"]
            })
            cust_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            print(f"✅ Customer created: {cust['customer_name']}")
        else:
            print(f"⚠ Customer already exists: {cust['customer_name']}")
