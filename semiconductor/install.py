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


def create_ai_chip_manufacturing_flow():
    # -----------------------------------------------------------
    # 2. Suppliers
    # -----------------------------------------------------------
    suppliers = [
        {"supplier_name": "TSMC Foundry", "supplier_type": "Manufacturing"},
        {"supplier_name": "ASE Group", "supplier_type": "Subcontractor"},
        {"supplier_name": "Intel Test Services", "supplier_type": "Testing"},
        {"supplier_name": "Material Supply Co.", "supplier_type": "Raw Material"},
    ]
    for s in suppliers:
        if not frappe.db.exists("Supplier", s["supplier_name"]):
            supplier_doc = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": s["supplier_name"],
                "supplier_group": s["supplier_type"]
            })
            supplier_doc.insert(ignore_permissions=True)
            print(f"🏭 Created Supplier: {s['supplier_name']}")

    # -----------------------------------------------------------
    # 3. Workstation Types and Workstations
    # -----------------------------------------------------------
    workstation_types = [
        "Wafer Fabrication", "Photolithography", "Etching / Metallization",
        "Dicing Workstation", "Packaging / Assembly", "Test Lab", "QA / Inspection"
    ]
    for ws in workstation_types:
        if not frappe.db.exists("Workstation", ws):
            frappe.get_doc({
                "doctype": "Workstation",
                "workstation_name": ws,
                "description": f"{ws} for AI Chip Manufacturing"
            }).insert(ignore_permissions=True)
            print(f"🔧 Created Workstation: {ws}")

    # -----------------------------------------------------------
    # 4. Operations
    # -----------------------------------------------------------
    operations = [
        {"operation_name": "Wafer Fabrication", "workstation": "Wafer Fabrication"},
        {"operation_name": "Photolithography", "workstation": "Photolithography"},
        {"operation_name": "Etching & Metallization", "workstation": "Etching / Metallization"},
        {"operation_name": "Wafer Dicing / Singulation", "workstation": "Dicing Workstation"},
        {"operation_name": "Chip Packaging", "workstation": "Packaging / Assembly"},
        {"operation_name": "Testing & Binning", "workstation": "Test Lab"},
        {"operation_name": "Final QA / Inspection", "workstation": "QA / Inspection"},
    ]

    for op in operations:
        if not frappe.db.exists("Operation", op["operation_name"]):
            frappe.get_doc({
                "doctype": "Operation",
                "operation_name": op["operation_name"],
                "workstation": op["workstation"],
                "description": f"{op['operation_name']} process for semiconductor chip"
            }).insert(ignore_permissions=True)
            print(f"⚙️ Created Operation: {op['operation_name']}")

    # -----------------------------------------------------------
    # 5. Sub-Assembly BOMs
    # -----------------------------------------------------------
    boms = [
        {
            "item": "AI Die",
            "items": [
                {"item_code": "SILICON-WAFER-300MM", "qty": 1},
                {"item_code": "PHOTORESIST-CHEM", "qty": 2},
                {"item_code": "DOPANT-PHOSPHORUS", "qty": 1},
                {"item_code": "DOPANT-BORON", "qty": 1},
                {"item_code": "ALUMINUM-METAL", "qty": 1},
                {"item_code": "COPPER-METAL", "qty": 1},
                {"item_code": "DIELECTRIC-HFO2", "qty": 1},
                {"item_code": "DIELECTRIC-SIO2", "qty": 1}
            ],
            "operations": [
                {"operation": "Wafer Fabrication", "workstation": "Wafer Fabrication"},
                {"operation": "Photolithography", "workstation": "Photolithography"},
                {"operation": "Etching & Metallization", "workstation": "Etching / Metallization"},
                {"operation": "Wafer Dicing / Singulation", "workstation": "Dicing Workstation"}
            ]
        },
        {
            "item": "AI Package Assembly",
            "items": [
                {"item_code": "AI Die", "qty": 1},
                {"item_code": "THERMAL-INTERFACE-MAT", "qty": 1},
                {"item_code": "MOLD-COMPOUND", "qty": 1},
                {"item_code": "SOLDER-BALLS", "qty": 1},
                {"item_code": "LEADFRAME-PACK", "qty": 1}
            ],
            "operations": [
                {"operation": "Chip Packaging", "workstation": "Packaging / Assembly"}
            ]
        },
        # {
        #     "item": "AI Inference Chip",
        #     "items": [
        #         {"item_code": "AI Package Assembly", "qty": 1}
        #     ],
        #     "operations": [
        #         {"operation": "Testing & Binning", "workstation": "Test Lab"},
        #         {"operation": "Final QA / Inspection", "workstation": "QA / Inspection"}
        #     ]
        # }
    ]

    for b in boms:
        if not frappe.db.exists("BOM", {"item": b["item"], "is_active": 1}):
            bom_doc = frappe.get_doc({
                "doctype": "BOM",
                "item": b["item"],
                "quantity": 1,
                "is_active": 1,
                "is_default": 1,
                "items": [{"item_code": i["item_code"], "qty": i["qty"]} for i in b["items"]],
                "operations": [{"operation": o["operation"], "workstation": o["workstation"], "time_in_mins": 60} for o in b["operations"]],
            })
            bom_doc.insert(ignore_permissions=True)
            print(f"🧩 Created BOM: {b['item']}")

    # -----------------------------------------------------------
    # 6. Purchase Orders for Raw Materials
    # -----------------------------------------------------------
    raw_materials = [
        {"item_code": "SILICON-WAFER-300MM", "qty": 100, "rate": 2000},
        {"item_code": "PHOTORESIST-CHEM", "qty": 500, "rate": 50},
        {"item_code": "DOPANT-PHOSPHORUS", "qty": 100, "rate": 150},
        {"item_code": "DOPANT-BORON", "qty": 100, "rate": 160},
        {"item_code": "ALUMINUM-METAL", "qty": 500, "rate": 120},
        {"item_code": "COPPER-METAL", "qty": 500, "rate": 100},
        {"item_code": "DIELECTRIC-HFO2", "qty": 100, "rate": 180},
        {"item_code": "DIELECTRIC-SIO2", "qty": 100, "rate": 160},
    ]

    if not frappe.db.exists("Purchase Order", {"supplier": "Material Supply Co."}):
        po = frappe.get_doc({
            "doctype": "Purchase Order",
            "supplier": "Material Supply Co.",
            "schedule_date": frappe.utils.nowdate(),
            "items": [{"item_code": i["item_code"], "qty": i["qty"], "rate": i["rate"]} for i in raw_materials]
        })
        po.insert(ignore_permissions=True)
        po.submit()
        print("🧾 Created Purchase Order for raw materials.")

    # -----------------------------------------------------------
    # 7. Subcontracting Orders
    # -----------------------------------------------------------
    subcontract_orders = [
        {
            "supplier": "ASE Group",
            "subcontracted_item": "AI Package Assembly",
            "qty": 5000,
            "rm_items": [
                {"item_code": "AI Die", "qty": 5000},
                {"item_code": "THERMAL-INTERFACE-MAT", "qty": 5000},
                {"item_code": "LEADFRAME-PACK", "qty": 5000},
            ]
        },
        {
            "supplier": "Intel Test Services",
            "subcontracted_item": "AI Inference Chip",
            "qty": 20000,
            "rm_items": [
                {"item_code": "AI Package Assembly", "qty": 20000}
            ]
        }
    ]

    # for sc in subcontract_orders:
    #     if not frappe.db.exists("Purchase Order", {"supplier": sc["supplier"], "is_subcontracted": 1}):
    #         po = frappe.get_doc({
    #             "doctype": "Purchase Order",
    #             "supplier": sc["supplier"],
    #             "is_subcontracted": 1,
    #             "items": [
    #                 {
    #                     "item_code": sc["subcontracted_item"],
    #                     "qty": sc["qty"],
    #                     "schedule_date": frappe.utils.nowdate()
    #                 }
    #             ],
    #             "supplied_items": sc["rm_items"]
    #         })
    #         po.insert(ignore_permissions=True)
    #         po.submit()
    #         print(f"🔧 Created Subcontract Order for {sc['subcontracted_item']} via {sc['supplier']}")

    frappe.db.commit()
    print("🎯 Full AI Chip Manufacturing Setup Complete!")


"""
ERPNext: Subcontracted Chip Manufacturing Full Flow Script
File: erpnext_subcontract_chip_flow.py
Run with: bench execute path.to.module:function_name

This script creates a baseline setup for a subcontracted chip manufacturing flow in ERPNext:
- Item Groups, UoMs, Warehouses, Suppliers
- Raw material Items and Finished Goods Items
- Service Item to represent subcontracted operations
- BOM (with raw material items)
- Work Order (Production Order)
- Material Request for raw materials
- Purchase Order to supplier (service item = subcontracting)
- Purchase Receipt and Purchase Invoice skeletons

Design notes / assumptions:
- This script is intentionally idempotent: it checks for existing docs and skips creation.
- "Subcontracting" here is modelled via a Service-type Purchase Order to a supplier (common pattern).
- Adjust field names/values to match your ERPNext version and company settings.

IMPORTANT: Test in a development site before running on production.
"""

import frappe
from frappe.utils import nowdate

# ----------------------
# Helpers
# ----------------------

def exists(doctype, name):
    return frappe.db.exists(doctype, name)


def create_item_group(name, parent=None):
    if exists('Item Group', name):
        return name
    doc = frappe.get_doc({
        'doctype': 'Item Group',
        'item_group_name': name,
        'parent_item_group': parent or 'All Item Groups'
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_uom(uom_name):
    if exists('UOM', uom_name):
        return uom_name
    doc = frappe.get_doc({'doctype': 'UOM', 'uom_name': uom_name})
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_warehouse(name, company='Default Company'):
    if exists('Warehouse', name):
        return name
    doc = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': name, 'company': company})
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_supplier(name, supplier_type='Company', country='India'):
    if exists('Supplier', name):
        return name
    doc = frappe.get_doc({
        'doctype': 'Supplier',
        'supplier_name': name,
        'supplier_type': supplier_type,
        'country': country
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.name


def create_item(item_code, item_name=None, item_group='Raw Materials', stock_uom='Nos', is_stock_item=1, item_type='Stock'):
    # item_type is for clarity; in ERPNext the key fields are is_stock_item, stock_uom, item_group
    if exists('Item', item_code):
        return item_code
    doc = frappe.get_doc({
        'doctype': 'Item',
        'item_code': item_code,
        'item_name': item_name or item_code,
        'item_group': item_group,
        'is_stock_item': is_stock_item,
        'stock_uom': stock_uom,
        'standard_rate': 0
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.item_code


def create_service_item(item_code, item_name=None, item_group='Services'):
    if exists('Item', item_code):
        return item_code
    doc = frappe.get_doc({
        'doctype': 'Item',
        'item_code': item_code,
        'item_name': item_name or item_code,
        'item_group': item_group,
        'is_stock_item': 0,
        'stock_uom': 'Nos'
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return doc.item_code


def create_bom(item_code, raw_materials, uom='Nos'):
    # raw_materials: list of dicts [{'item_code':..., 'qty':...}, ...]
    if frappe.db.exists('BOM', {'item': item_code}):
        return frappe.db.get_value('BOM', {'item': item_code})

    bom = frappe.get_doc({
        'doctype': 'BOM',
        'item': item_code,
        'is_default': 1,
        'quantity': 1.0,
        'items': [{'item_code': r['item_code'], 'qty': r['qty'], 'uom': uom} for r in raw_materials]
    })
    bom.insert(ignore_permissions=True)
    bom.submit()
    frappe.db.commit()
    return bom.name


def create_work_order(item_code, qty=1, bom_no=None, fg_warehouse=None):
    # Work Order doctype is 'Work Order' in many ERPNext versions
    filters = {'production_item': item_code}
    if frappe.db.exists('Work Order', filters):
        return frappe.db.get_value('Work Order', filters)

    wo = frappe.get_doc({
        'doctype': 'Work Order',
        'production_item': item_code,
        'qty': qty,
        'bom_no': bom_no or '',
        'fg_warehouse': fg_warehouse or ''
    })
    wo.insert(ignore_permissions=True)
    frappe.db.commit()
    return wo.name


def create_material_request_for_bom_item(item_code, qty, schedule_date=None, warehouse=None):
    mr_name = f"MR-{item_code}-{nowdate()}-{qty}"
    # We'll search existing MR
    existing = frappe.db.get_value('Material Request', {'material_request_type': 'Material Transfer', 'title': mr_name})
    if existing:
        return existing

    mr = frappe.get_doc({
        'doctype': 'Material Request',
        'material_request_type': 'Material Transfer',
        'title': mr_name,
        'transaction_date': nowdate(),
        'schedule_date': schedule_date or nowdate(),
        'items': [{'item_code': item_code, 'qty': qty, 'uom': 'Nos', 'warehouse': warehouse or ''}]
    })
    mr.insert(ignore_permissions=True)
    frappe.db.commit()
    return mr.name


def create_purchase_order(supplier, items, transaction_date=None):
    # items: list of dicts: [{'item_code':..., 'qty':..., 'rate':...}]
    po_doc = frappe.get_doc({
        'doctype': 'Purchase Order',
        'supplier': supplier,
        'transaction_date': transaction_date or nowdate(),
        'schedule_date': transaction_date or nowdate(),
        'items': [{'item_code': i['item_code'], 'qty': i['qty'], 'rate': i.get('rate', 0)} for i in items]
    })
    po_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return po_doc.name


def create_purchase_receipt(po_name):
    # Create a Purchase Receipt skeleton from PO
    pr = frappe.get_doc({
        'doctype': 'Purchase Receipt',
        'supplier': frappe.db.get_value('Purchase Order', po_name, 'supplier'),
        'posting_date': nowdate(),
        'items': []
    })
    po_items = frappe.get_all('Purchase Order Item', filters={'parent': po_name}, fields=['item_code', 'qty'])
    for it in po_items:
        pr.append('items', {'item_code': it.item_code, 'qty': it.qty, 'received_qty': it.qty})
    pr.insert(ignore_permissions=True)
    frappe.db.commit()
    return pr.name


def create_purchase_invoice_from_pr(pr_name):
    pi = frappe.get_doc({
        'doctype': 'Purchase Invoice',
        'supplier': frappe.db.get_value('Purchase Receipt', pr_name, 'supplier'),
        'posting_date': nowdate(),
        'items': []
    })
    pr_items = frappe.get_all('Purchase Receipt Item', filters={'parent': pr_name}, fields=['item_code', 'qty'])
    for it in pr_items:
        pi.append('items', {'item_code': it.item_code, 'qty': it.qty, 'rate': 0})
    pi.insert(ignore_permissions=True)
    frappe.db.commit()
    return pi.name


# ----------------------
# Main orchestration
# ----------------------

def setup_subcontracted_chip_flow():
    """Main function to bootstrap a sample subcontracted chip manufacturing flow."""
    frappe.flags.ignore_permissions = True

    # 1) Basic master data
    create_item_group('Raw Materials', parent='All Item Groups')
    create_item_group('Finished Goods', parent='All Item Groups')
    create_item_group('Services', parent='All Item Groups')

    create_uom('Nos')
    create_uom('Gram')

    company = frappe.db.get_value('Global Defaults', None, 'default_company') or frappe.db.get_value('Company')
    if not company:
        company = 'Default Company'

    create_warehouse('Raw Warehouse - RIT', company=company)
    create_warehouse('FG Warehouse - RIT', company=company)

    supplier_name = 'Subcontractor Co.'
    create_supplier(supplier_name)

    # 2) Create items: an example finished chip and some raw materials
    fg_item = 'CHIP-FULL-1000'
    create_item(fg_item, item_group='Finished Goods', stock_uom='Nos')

    raw1 = 'WAFER-12inch'
    raw2 = 'PACKAGING-MATERIAL'
    create_item(raw1, item_group='Raw Materials', stock_uom='Nos')
    create_item(raw2, item_group='Raw Materials', stock_uom='Nos')

    # Service item to represent subcontracted processing (e.g. wafer fab, packaging, test)
    svc_item = f'SUBCONTRACT-PROCESS-{fg_item}'
    create_service_item(svc_item, item_group='Services')

    # 3) BOM for FG item (uses raw1 and raw2)
    bom_name = create_bom(fg_item, [{'item_code': raw1, 'qty': 1}, {'item_code': raw2, 'qty': 2}])

    # 4) Create a Work Order to manufacture FG
    wo_name = create_work_order(fg_item, qty=100, bom_no=bom_name, fg_warehouse='FG Warehouse - RIT')

    # 5) Material Request for raw items (simple MR)
    mr1 = create_material_request_for_bom_item(raw1, qty=100, warehouse='Raw Warehouse - RIT')
    mr2 = create_material_request_for_bom_item(raw2, qty=200, warehouse='Raw Warehouse - RIT')

    # 6) Create Purchase Order to subcontractor for service (subcontracting)
    po_name = create_purchase_order(supplier_name, [{'item_code': svc_item, 'qty': 1, 'rate': 10000}])

    # 7) Purchase Receipt and Invoice after subcontracting done
    pr_name = create_purchase_receipt(po_name)
    pi_name = create_purchase_invoice_from_pr(pr_name)

    frappe.db.commit()

    out = {
        'company': company,
        'fg_item': fg_item,
        'raw_items': [raw1, raw2],
        'service_item': svc_item,
        'bom': bom_name,
        'work_order': wo_name,
        'material_requests': [mr1, mr2],
        'purchase_order': po_name,
        'purchase_receipt': pr_name,
        'purchase_invoice': pi_name
    }
    frappe.msgprint('Subcontracted chip flow setup completed. See bench console for details.')
    print('\n=== Subcontracted Flow Created ===')
    for k, v in out.items():
        print(f"{k}: {v}")
    return out


# Optional: allow bench execute to call
def execute():
    return setup_subcontracted_chip_flow()
