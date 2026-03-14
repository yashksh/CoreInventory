"""
CoreInventory — Seed Data for User 4 (Maithil) & User 5 (Myth12)
Covers ALL conditions: draft, waiting, ready, done | receipt, delivery, internal
Usage: python seed_users.py
"""

from app import app, db
from models import (
    Warehouse, Location, Contact, Product,
    Inventory, StockMove, StockMoveLine, MoveHistory,
)
from datetime import datetime


def seed():
    with app.app_context():

        # ── Ensure shared master data exists ──────────────────

        # Warehouses
        wh_data = [
            ('Main Warehouse',      'WH', '12 Industrial Estate, Ahmedabad'),
            ('North Distribution',  'ND', '45 Logistics Park, Delhi'),
            ('South Hub',           'SH', '78 Trade Centre, Chennai'),
        ]
        for name, code, addr in wh_data:
            if not Warehouse.query.filter_by(short_code=code).first():
                db.session.add(Warehouse(name=name, short_code=code, address=addr))
        db.session.commit()
        wh = {w.short_code: w.id for w in Warehouse.query.all()}

        # Locations
        loc_data = [
            (wh['WH'], 'Stock Zone A',   'WH/Stock-A'),
            (wh['WH'], 'Stock Zone B',   'WH/Stock-B'),
            (wh['WH'], 'Receiving Dock', 'WH/Recv'),
            (wh['WH'], 'Shipping Dock',  'WH/Ship'),
            (wh['ND'], 'Shelf 1',        'ND/Shelf-1'),
            (wh['ND'], 'Shelf 2',        'ND/Shelf-2'),
            (wh['ND'], 'Cold Storage',   'ND/Cold'),
            (wh['SH'], 'Bay A',          'SH/Bay-A'),
            (wh['SH'], 'Bay B',          'SH/Bay-B'),
            (wh['SH'], 'Returns Area',   'SH/Returns'),
        ]
        for wid, name, code in loc_data:
            if not Location.query.filter_by(short_code=code).first():
                db.session.add(Location(warehouse_id=wid, name=name, short_code=code))
        db.session.commit()

        # Contacts
        con_data = [
            ('Azure Interior',       'vendor',   'sales@azureinterior.com',      '+91 79 2345 6789'),
            ('Steel Craft Supplies', 'vendor',   'orders@steelcraft.in',         '+91 22 4567 8901'),
            ('TimberWorks India',    'vendor',   'info@timberworks.co.in',       '+91 80 3456 7890'),
            ('PackRight Solutions',  'vendor',   'contact@packright.com',        '+91 44 5678 9012'),
            ('Nova Electronics',     'vendor',   'procurement@novaelec.in',      '+91 11 6789 0123'),
            ('Pinnacle Furnishings', 'customer', 'buying@pinnacle.co.in',        '+91 79 7890 1234'),
            ('Metro Office Hub',     'customer', 'orders@metrooffice.com',       '+91 22 8901 2345'),
            ('GreenLeaf Interiors',  'customer', 'design@greenleaf.in',          '+91 80 9012 3456'),
            ('Skyline Commercial',   'customer', 'procurement@skylinecomm.com',  '+91 11 0123 4567'),
            ('Coastal Retail Group', 'customer', 'supply@coastalretail.in',      '+91 44 1234 5678'),
        ]
        for name, ctype, email, phone in con_data:
            if not Contact.query.filter_by(email=email).first():
                db.session.add(Contact(name=name, type=ctype, email=email, phone=phone))
        db.session.commit()

        # Products
        prod_data = [
            ('DESK001',  'Executive Office Desk',      12500),
            ('TABLE001', 'Conference Table 8-Seater',   18500),
            ('CHAIR001', 'Ergonomic Mesh Chair',         8750),
            ('CHAIR002', 'Visitor Stacking Chair',       2200),
            ('CAB001',   'Filing Cabinet 4-Drawer',      6800),
            ('SHELF001', 'Industrial Metal Shelving',    4500),
            ('MON001',   '27" 4K Monitor',              22000),
            ('KEY001',   'Wireless Keyboard + Mouse',    1800),
            ('LAMP001',  'LED Desk Lamp Adjustable',     1200),
            ('WHTBRD01', 'Magnetic Whiteboard 6x4',      3500),
            ('PROJ001',  'HD Projector 4000 Lumens',    35000),
            ('CABLE01',  'CAT6 Ethernet Cable 50m',       850),
            ('PAPER01',  'A4 Copier Paper (5 Reams)',      750),
            ('TONER01',  'Laser Printer Toner Black',    2800),
            ('LOCK001',  'Combination Padlock Heavy',      650),
        ]
        for code, name, cost in prod_data:
            if not Product.query.filter_by(product_code=code).first():
                db.session.add(Product(product_code=code, name=name, unit_cost=cost))
        db.session.commit()
        print('✔ Master data ready')

        # Lookup maps
        prods = {p.product_code: p for p in Product.query.all()}
        locs  = {l.short_code: l  for l in Location.query.all()}
        cons  = {c.name: c        for c in Contact.query.all()}

        # ── Inventory (shared) ────────────────────────────────
        inv_data = [
            ('DESK001','WH/Stock-A', 45), ('DESK001','ND/Shelf-1', 20), ('DESK001','SH/Bay-A', 12),
            ('TABLE001','WH/Stock-A',30), ('TABLE001','WH/Stock-B',15), ('TABLE001','SH/Bay-A', 8),
            ('CHAIR001','WH/Stock-A',120),('CHAIR001','ND/Shelf-1',60), ('CHAIR001','SH/Bay-A',40),
            ('CHAIR002','WH/Stock-A',200),('CHAIR002','ND/Shelf-1',80), ('CHAIR002','SH/Bay-B',50),
            ('CAB001','WH/Stock-B',  35), ('CAB001','ND/Shelf-2',  25),
            ('SHELF001','WH/Stock-B',50), ('SHELF001','ND/Shelf-1',30), ('SHELF001','SH/Bay-A',20),
            ('MON001','WH/Stock-A',  80), ('MON001','ND/Shelf-2',  45),
            ('KEY001','WH/Stock-A', 150), ('KEY001','ND/Shelf-1',  70), ('KEY001','SH/Bay-B', 35),
            ('LAMP001','WH/Stock-B', 60), ('LAMP001','ND/Shelf-2', 40),
            ('WHTBRD01','WH/Stock-A',25), ('WHTBRD01','SH/Bay-A',  10),
            ('PROJ001','WH/Stock-B', 15), ('PROJ001','SH/Bay-B',    5),
            ('CABLE01','WH/Stock-A',200), ('CABLE01','ND/Shelf-1', 100),
            ('PAPER01','WH/Stock-B',500), ('PAPER01','ND/Shelf-2', 300),('PAPER01','SH/Bay-B',200),
            ('TONER01','WH/Stock-B', 40), ('TONER01','ND/Shelf-2',  20),
            ('LOCK001','WH/Stock-A', 90), ('LOCK001','ND/Shelf-1',  60),('LOCK001','SH/Bay-A', 30),
        ]
        for pcode, lcode, qty in inv_data:
            p = prods[pcode]; l = locs[lcode]
            existing = Inventory.query.filter_by(product_id=p.id, location_id=l.id).first()
            if existing:
                existing.quantity = qty
            else:
                db.session.add(Inventory(product_id=p.id, location_id=l.id, quantity=qty))
        db.session.commit()
        print('✔ Inventory ready')

        # ═══════════════════════════════════════════════════════
        #  STOCK MOVES for USER 4 (Maithil) — uid=4
        # ═══════════════════════════════════════════════════════
        uid4 = 4

        moves_user4 = [
            # ── RECEIPTS ──────────────────────────────────────
            # done
            ('M/IN/00001','receipt','Azure Interior',     None,'WH/Stock-A','2026-02-08','done',
             [('DESK001',25),('CHAIR001',50),('LAMP001',20)]),
            ('M/IN/00002','receipt','Steel Craft Supplies',None,'WH/Stock-B','2026-02-14','done',
             [('CAB001',15),('SHELF001',25),('LOCK001',40)]),
            ('M/IN/00003','receipt','Nova Electronics',    None,'ND/Shelf-1','2026-02-22','done',
             [('MON001',30),('KEY001',45),('CABLE01',80)]),
            # ready
            ('M/IN/00004','receipt','TimberWorks India',   None,'WH/Stock-A','2026-03-16','ready',
             [('TABLE001',12),('CHAIR002',60)]),
            ('M/IN/00005','receipt','PackRight Solutions',  None,'SH/Bay-A','2026-03-18','ready',
             [('PAPER01',300),('TONER01',25)]),
            # waiting
            ('M/IN/00006','receipt','Azure Interior',      None,'ND/Shelf-2','2026-03-20','waiting',
             [('DESK001',18),('WHTBRD01',10)]),
            # draft
            ('M/IN/00007','receipt','Nova Electronics',    None,'WH/Stock-A','2026-03-25','draft',
             [('PROJ001',8),('MON001',20),('CABLE01',50)]),

            # ── DELIVERIES ────────────────────────────────────
            # done
            ('M/OUT/00001','delivery','Pinnacle Furnishings','WH/Stock-A',None,'2026-02-10','done',
             [('DESK001',10),('CHAIR001',30)]),
            ('M/OUT/00002','delivery','Metro Office Hub',    'WH/Stock-A',None,'2026-02-20','done',
             [('MON001',15),('KEY001',40),('LAMP001',10)]),
            ('M/OUT/00003','delivery','GreenLeaf Interiors',  'ND/Shelf-1',None,'2026-03-01','done',
             [('TABLE001',5),('SHELF001',12)]),
            # ready
            ('M/OUT/00004','delivery','Skyline Commercial','SH/Bay-A',None,'2026-03-17','ready',
             [('CHAIR002',35),('LOCK001',20)]),
            ('M/OUT/00005','delivery','Coastal Retail Group','WH/Stock-B',None,'2026-03-19','ready',
             [('CAB001',10),('TONER01',15)]),
            # waiting
            ('M/OUT/00006','delivery','Pinnacle Furnishings','WH/Stock-A',None,'2026-03-22','waiting',
             [('DESK001',20),('PROJ001',3)]),
            # draft
            ('M/OUT/00007','delivery','Metro Office Hub','ND/Shelf-2',None,'2026-03-28','draft',
             [('PAPER01',200),('SHELF001',8)]),

            # ── INTERNAL TRANSFERS ────────────────────────────
            # done
            ('M/INT/00001','internal',None,'WH/Stock-A','ND/Shelf-1','2026-03-02','done',
             [('CHAIR001',25),('KEY001',20)]),
            # ready
            ('M/INT/00002','internal',None,'ND/Shelf-1','SH/Bay-A','2026-03-16','ready',
             [('CHAIR002',40),('CABLE01',30)]),
            # waiting
            ('M/INT/00003','internal',None,'WH/Stock-B','SH/Bay-B','2026-03-21','waiting',
             [('LAMP001',15),('TONER01',10)]),
            # draft
            ('M/INT/00004','internal',None,'WH/Stock-A','WH/Stock-B','2026-03-26','draft',
             [('MON001',10),('WHTBRD01',5)]),
        ]

        # ═══════════════════════════════════════════════════════
        #  STOCK MOVES for USER 5 (Myth12) — uid=5
        # ═══════════════════════════════════════════════════════
        uid5 = 5

        moves_user5 = [
            # ── RECEIPTS ──────────────────────────────────────
            # done
            ('Y/IN/00001','receipt','TimberWorks India',   None,'WH/Stock-A','2026-02-05','done',
             [('TABLE001',20),('CHAIR002',80)]),
            ('Y/IN/00002','receipt','PackRight Solutions',  None,'ND/Shelf-2','2026-02-18','done',
             [('PAPER01',400),('TONER01',30),('LOCK001',50)]),
            ('Y/IN/00003','receipt','Azure Interior',      None,'SH/Bay-A','2026-03-03','done',
             [('DESK001',15),('CHAIR001',40),('WHTBRD01',12)]),
            # ready
            ('Y/IN/00004','receipt','Steel Craft Supplies', None,'WH/Stock-B','2026-03-15','ready',
             [('SHELF001',35),('CAB001',20)]),
            ('Y/IN/00005','receipt','Nova Electronics',     None,'ND/Shelf-1','2026-03-18','ready',
             [('MON001',25),('KEY001',60),('CABLE01',100)]),
            # waiting
            ('Y/IN/00006','receipt','TimberWorks India',    None,'WH/Stock-A','2026-03-22','waiting',
             [('TABLE001',15),('CHAIR001',30)]),
            # draft
            ('Y/IN/00007','receipt','PackRight Solutions',  None,'SH/Bay-B','2026-03-27','draft',
             [('PAPER01',250),('LAMP001',30),('PROJ001',5)]),

            # ── DELIVERIES ────────────────────────────────────
            # done
            ('Y/OUT/00001','delivery','GreenLeaf Interiors','WH/Stock-A',None,'2026-02-12','done',
             [('DESK001',8),('CHAIR001',20),('LAMP001',15)]),
            ('Y/OUT/00002','delivery','Skyline Commercial', 'ND/Shelf-1',None,'2026-02-25','done',
             [('KEY001',35),('SHELF001',10)]),
            ('Y/OUT/00003','delivery','Coastal Retail Group','SH/Bay-A', None,'2026-03-05','done',
             [('CHAIR002',30),('LOCK001',18),('WHTBRD01',6)]),
            # ready
            ('Y/OUT/00004','delivery','Pinnacle Furnishings','WH/Stock-A',None,'2026-03-17','ready',
             [('TABLE001',8),('DESK001',12)]),
            ('Y/OUT/00005','delivery','Metro Office Hub', 'WH/Stock-B', None,'2026-03-20','ready',
             [('CAB001',12),('TONER01',18)]),
            # waiting
            ('Y/OUT/00006','delivery','GreenLeaf Interiors','ND/Shelf-2',None,'2026-03-24','waiting',
             [('PAPER01',150),('MON001',10)]),
            # draft
            ('Y/OUT/00007','delivery','Skyline Commercial','WH/Stock-A', None,'2026-03-30','draft',
             [('CHAIR001',45),('PROJ001',4),('CABLE01',60)]),

            # ── INTERNAL TRANSFERS ────────────────────────────
            # done
            ('Y/INT/00001','internal',None,'WH/Stock-A','SH/Bay-A','2026-02-28','done',
             [('DESK001',10),('CHAIR002',25)]),
            ('Y/INT/00002','internal',None,'ND/Shelf-1','WH/Stock-B','2026-03-08','done',
             [('KEY001',15),('SHELF001',8)]),
            # ready
            ('Y/INT/00003','internal',None,'WH/Stock-B','ND/Shelf-2','2026-03-18','ready',
             [('LAMP001',20),('TONER01',12)]),
            # waiting
            ('Y/INT/00004','internal',None,'SH/Bay-A','WH/Stock-A','2026-03-23','waiting',
             [('CHAIR001',15),('LOCK001',10)]),
            # draft
            ('Y/INT/00005','internal',None,'WH/Stock-A','ND/Shelf-1','2026-03-29','draft',
             [('MON001',12),('CABLE01',40),('WHTBRD01',8)]),
        ]

        # ── INSERT HELPER ─────────────────────────────────────
        def insert_moves(uid, moves_data, label):
            for ref, optype, contact_name, from_loc, to_loc, sdate, status, lines in moves_data:
                # Skip if already exists
                if StockMove.query.filter_by(reference=ref).first():
                    continue

                m = StockMove(
                    reference=ref,
                    operation_type=optype,
                    contact_id=cons[contact_name].id if contact_name else None,
                    from_location_id=locs[from_loc].id if from_loc else None,
                    to_location_id=locs[to_loc].id if to_loc else None,
                    schedule_date=datetime.strptime(sdate, '%Y-%m-%d').date(),
                    status=status,
                    created_by=uid,
                )
                db.session.add(m)
                db.session.flush()

                for pcode, qty in lines:
                    db.session.add(StockMoveLine(
                        move_id=m.id,
                        product_id=prods[pcode].id,
                        quantity=qty,
                    ))

                # Move history for done operations
                if status == 'done':
                    for pcode, qty in lines:
                        db.session.add(MoveHistory(
                            move_id=m.id,
                            product_id=prods[pcode].id,
                            from_location_id=locs[from_loc].id if from_loc else None,
                            to_location_id=locs[to_loc].id if to_loc else None,
                            quantity=qty,
                        ))

            db.session.commit()
            print(f'✔ Moves seeded for {label}')

        # ── RUN ───────────────────────────────────────────────
        insert_moves(uid4, moves_user4, 'User 4 (Maithil)')
        insert_moves(uid5, moves_user5, 'User 5 (Myth12)')

        print('\n🎉 All seed data inserted for both users!')


if __name__ == '__main__':
    seed()
