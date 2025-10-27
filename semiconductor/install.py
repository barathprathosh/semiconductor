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
        "Alpha Infotech Pvt. Ltd.",
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
            "customer": "Alpha Infotech Pvt. Ltd.",
            "transaction_date": add_days(nowdate(), -60),
            "delivery_date": add_days(nowdate(), -45),
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
        {"customer_name": "Alpha Infotech Pvt. Ltd.", "customer_group": "Commercial", "territory": "India"},
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

import frappe

def AI_chip_manufacturing_data():
    # ---------- 1. Create Customers ----------
    customers = [
        {"customer_name": "Techtronics AI Systems"},
        {"customer_name": "NeuroEdge Computing"},
    ]
    for c in customers:
        if not frappe.db.exists("Customer", c["customer_name"]):
            doc = frappe.get_doc({
                "doctype": "Customer",
                "customer_name": c["customer_name"],
                "customer_type": "Company"
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    # ---------- 2. Create Suppliers ----------
    suppliers = [
        {"supplier_name": "Silicon Materials Ltd"},
        {"supplier_name": "NanoFab Chemicals Pvt Ltd"},
        {"supplier_name": "PackTech Electronics"},
    ]
    for s in suppliers:
        if not frappe.db.exists("Supplier", s["supplier_name"]):
            doc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": s["supplier_name"],
                "supplier_type": "Company"
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()

    # ---------- 3. Create Workstation Types ----------
    workstation_types = [
        "Cleanroom – Wafer Fab Line",
        "Photolithography Cell",
        "Etching/Deposition Station",
        "Dicing & Sawing Station",
        "Assembly & Packaging Line",
        "ATE Lab",
        "QA & Reliability Lab"
    ]
    for wtype in workstation_types:
        if not frappe.db.exists("Workstation Type", wtype):
            frappe.get_doc({
                "doctype": "Workstation Type",
                "workstation_type": wtype
            }).insert(ignore_permissions=True)

    # ---------- 4. Create Workstations ----------
    workstations = [
        {"name": "Wafer Fab Line", "type": "Cleanroom – Wafer Fab Line", "rate": 5000},
        {"name": "Photolithography Workstation", "type": "Photolithography Cell", "rate": 4000},
        {"name": "Etching Station", "type": "Etching/Deposition Station", "rate": 4500},
        {"name": "Dicing Workstation", "type": "Dicing & Sawing Station", "rate": 3000},
        {"name": "Packaging Line", "type": "Assembly & Packaging Line", "rate": 3500},
        {"name": "ATE Lab", "type": "ATE Lab", "rate": 6000},
        {"name": "QA Inspection Lab", "type": "QA & Reliability Lab", "rate": 2500},
    ]
    for w in workstations:
        if not frappe.db.exists("Workstation", w["name"]):
            frappe.get_doc({
                "doctype": "Workstation",
                "workstation_name": w["name"],
                "workstation_type": w["type"],
                "hour_rate": w["rate"],
                "production_capacity": 100,
            }).insert(ignore_permissions=True)

    # ---------- 5. Create Items ----------
    items = [
        # Finished Good
        {"item_code": "AI-INFERENCE-CHIP-7NM-300W", "item_name": "AI Inference Chip 7nm 300W", "item_group": "Products", "stock_uom": "Nos", "is_stock_item": 1},
        # Raw Materials
        {"item_code": "SILICON-WAFER-300MM", "item_group": "Raw Material", "stock_uom": "Nos"},
        {"item_code": "DIELECTRIC-SIO2", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "DIELECTRIC-HFO2", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "COPPER-METAL", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "ALUMINUM-METAL", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "DOPANT-BORON", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "DOPANT-PHOSPHORUS", "item_group": "Raw Material", "stock_uom": "Gram"},
        {"item_code": "PHOTORESIST-CHEM", "item_group": "Consumable", "stock_uom": "Gram"},
        # Semi-Finished / Packaging
        {"item_code": "LEADFRAME-PACK", "item_group": "Sub Assemblies", "stock_uom": "Nos"},
        {"item_code": "SOLDER-BALLS", "item_group": "Sub Assemblies", "stock_uom": "Gram"},
        {"item_code": "MOLD-COMPOUND", "item_group": "Sub Assemblies", "stock_uom": "Gram"},
        {"item_code": "THERMAL-INTERFACE-MAT", "item_group": "Sub Assemblies", "stock_uom": "Gram"},
    ]
    for i in items:
        if not frappe.db.exists("Item", i["item_code"]):
            frappe.get_doc({
                "doctype": "Item",
                "item_code": i["item_code"],
                "item_name": i.get("item_name", i["item_code"]),
                "item_group": i["item_group"],
                "stock_uom": i["stock_uom"],
                "is_stock_item": i.get("is_stock_item", 1)
            }).insert(ignore_permissions=True)

    # ---------- 6. Create Operations ----------
    operations = [
        ("Wafer Fabrication", "Wafer Fab Line", 10),
        ("Photolithography", "Photolithography Workstation", 8),
        ("Etching & Metallization", "Etching Station", 12),
        ("Wafer Dicing / Singulation", "Dicing Workstation", 6),
        ("Chip Packaging", "Packaging Line", 15),
        ("Testing & Binning", "ATE Lab", 20),
        ("Final QA / Inspection", "QA Inspection Lab", 6)
    ]
    op_docs = []
    for op_name, ws, time in operations:
        if not frappe.db.exists("Operation", op_name):
            doc = frappe.get_doc({
                "doctype": "Operation",
                "__newname": op_name,
                "operation_name": op_name,
                "workstation": ws,
                "description": f"{op_name} process for AI Inference Chip",
                "time_in_mins": time * 60
            })
            doc.insert(ignore_permissions=True)
            op_docs.append(doc.name)
        else:
            op_docs.append(op_name)

        # ---------- 7. Create BoM ----------
    if not frappe.db.exists("BOM", {"item": "AI-INFERENCE-CHIP-7NM-300W"}):
        bom = frappe.get_doc({
            "doctype": "BOM",
            "item": "AI-INFERENCE-CHIP-7NM-300W",
            "quantity": 20000,
            "uom": "Nos",
            "with_operations": 1,
            "items": [
                {"item_code": "SILICON-WAFER-300MM", "qty": 5, "uom": "Nos"},
                {"item_code": "DIELECTRIC-SIO2", "qty": 1000, "uom": "Gram"},
                {"item_code": "DIELECTRIC-HFO2", "qty": 400, "uom": "Gram"},
                {"item_code": "COPPER-METAL", "qty": 4000, "uom": "Gram"},
                {"item_code": "ALUMINUM-METAL", "qty": 2000, "uom": "Gram"},
                {"item_code": "DOPANT-BORON", "qty": 100, "uom": "Gram"},
                {"item_code": "DOPANT-PHOSPHORUS", "qty": 100, "uom": "Gram"},
                {"item_code": "PHOTORESIST-CHEM", "qty": 200, "uom": "Gram"},
                {"item_code": "LEADFRAME-PACK", "qty": 20000, "uom": "Nos"},
                {"item_code": "SOLDER-BALLS", "qty": 10000, "uom": "Gram"},
                {"item_code": "MOLD-COMPOUND", "qty": 4000, "uom": "Gram"},
                {"item_code": "THERMAL-INTERFACE-MAT", "qty": 1000, "uom": "Gram"},
            ],
            "operations": [
                {"operation": "Wafer Fabrication", "workstation": "Wafer Fab Line", "time_in_mins": 600},
                {"operation": "Photolithography", "workstation": "Photolithography Workstation", "time_in_mins": 480},
                {"operation": "Etching & Metallization", "workstation": "Etching Station", "time_in_mins": 720},
                {"operation": "Wafer Dicing / Singulation", "workstation": "Dicing Workstation", "time_in_mins": 360},
                {"operation": "Chip Packaging", "workstation": "Packaging Line", "time_in_mins": 900},
                {"operation": "Testing & Binning", "workstation": "ATE Lab", "time_in_mins": 1200},
                {"operation": "Final QA / Inspection", "workstation": "QA Inspection Lab", "time_in_mins": 360},
            ]
        })
        bom.insert(ignore_permissions=True)
        bom.submit()
        frappe.db.commit()

    frappe.msgprint("✅ AI Inference Chip Master Data Created Successfully!")
