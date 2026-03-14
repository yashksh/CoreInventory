"""
CoreInventory — Seed Data Script
Run this to populate the database with realistic demo data.
Usage: python seed_data.py
"""
from app import app, db
from models import (
    User, Warehouse, Location, Contact, Product,
    Inventory, StockMove, StockMoveLine, MoveHistory
)
from werkzeug.security import generate_password_hash
from datetime import date, datetime

def seed():
    with app.app_context():
        # ── ADMIN USER ─────────────────────────────────────────
        if not User.query.filter_by(login_id='admin').first():
            db.session.add(User(
                login_id='admin',
                email='admin@coreinventory.com',
                password_hash=generate_password_hash('admin123')
            ))
            db.session.commit()
            print('✔ Admin user created')

        admin = User.query.filter_by(login_id='admin').first()
        uid = admin.id

        # ── WAREHOUSES ─────────────────────────────────────────
        wh_data = [
            ('Main Warehouse', 'WH', '12 Industrial Estate, Ahmedabad'),
            ('North Distribution', 'ND', '45 Logistics Park, Delhi'),
            ('South Hub', 'SH', '78 Trade Centre, Chennai'),
        ]
        for name, code, addr in wh_data:
            if not Warehouse.query.filter_by(short_code=code).first():
                db.session.add(Warehouse(name=name, short_code=code, address=addr))
        db.session.commit()
        print('✔ Warehouses seeded')

        # ── LOCATIONS ──────────────────────────────────────────
        wh = {w.short_code: w.id for w in Warehouse.query.all()}
        loc_data = [
            (wh['WH'], 'Stock Zone A',  'WH/Stock-A'),
            (wh['WH'], 'Stock Zone B',  'WH/Stock-B'),
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
        print('✔ Locations seeded')

        # ── CONTACTS ───────────────────────────────────────────
        con_data = [
            ('Azure Interior',      'vendor',   'sales@azureinterior.com',     '+91 79 2345 6789'),
            ('Steel Craft Supplies', 'vendor',   'orders@steelcraft.in',        '+91 22 4567 8901'),
            ('TimberWorks India',    'vendor',   'info@timberworks.co.in',      '+91 80 3456 7890'),
            ('PackRight Solutions',  'vendor',   'contact@packright.com',       '+91 44 5678 9012'),
            ('Nova Electronics',     'vendor',   'procurement@novaelec.in',     '+91 11 6789 0123'),
            ('Pinnacle Furnishings', 'customer', 'buying@pinnacle.co.in',       '+91 79 7890 1234'),
            ('Metro Office Hub',     'customer', 'orders@metrooffice.com',      '+91 22 8901 2345'),
            ('GreenLeaf Interiors',  'customer', 'design@greenleaf.in',         '+91 80 9012 3456'),
            ('Skyline Commercial',   'customer', 'procurement@skylinecomm.com', '+91 11 0123 4567'),
            ('Coastal Retail Group', 'customer', 'supply@coastalretail.in',     '+91 44 1234 5678'),
        ]
        for name, ctype, email, phone in con_data:
            if not Contact.query.filter_by(email=email).first():
                db.session.add(Contact(name=name, type=ctype, email=email, phone=phone))
        db.session.commit()
        print('✔ Contacts seeded')

        # ── PRODUCTS ───────────────────────────────────────────
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
        print('✔ Products seeded')

        # lookup maps
        prods = {p.product_code: p for p in Product.query.all()}
        locs  = {l.short_code: l for l in Location.query.all()}
        cons  = {c.name: c for c in Contact.query.all()}

        # ── INVENTORY ──────────────────────────────────────────
        inv_data = [
            ('DESK001','WH/Stock-A',45), ('DESK001','ND/Shelf-1',20), ('DESK001','SH/Bay-A',12),
            ('TABLE001','WH/Stock-A',30), ('TABLE001','WH/Stock-B',15), ('TABLE001','SH/Bay-A',8),
            ('CHAIR001','WH/Stock-A',120), ('CHAIR001','ND/Shelf-1',60), ('CHAIR001','SH/Bay-A',40),
            ('CHAIR002','WH/Stock-A',200), ('CHAIR002','ND/Shelf-1',80), ('CHAIR002','SH/Bay-B',50),
            ('CAB001','WH/Stock-B',35), ('CAB001','ND/Shelf-2',25),
            ('SHELF001','WH/Stock-B',50), ('SHELF001','ND/Shelf-1',30), ('SHELF001','SH/Bay-A',20),
            ('MON001','WH/Stock-A',80), ('MON001','ND/Shelf-2',45),
            ('KEY001','WH/Stock-A',150), ('KEY001','ND/Shelf-1',70), ('KEY001','SH/Bay-B',35),
            ('LAMP001','WH/Stock-B',60), ('LAMP001','ND/Shelf-2',40),
            ('WHTBRD01','WH/Stock-A',25), ('WHTBRD01','SH/Bay-A',10),
            ('PROJ001','WH/Stock-B',15), ('PROJ001','SH/Bay-B',5),
            ('CABLE01','WH/Stock-A',200), ('CABLE01','ND/Shelf-1',100),
            ('PAPER01','WH/Stock-B',500), ('PAPER01','ND/Shelf-2',300), ('PAPER01','SH/Bay-B',200),
            ('TONER01','WH/Stock-B',40), ('TONER01','ND/Shelf-2',20),
            ('LOCK001','WH/Stock-A',90), ('LOCK001','ND/Shelf-1',60), ('LOCK001','SH/Bay-A',30),
        ]
        for pcode, lcode, qty in inv_data:
            p = prods[pcode]; l = locs[lcode]
            existing = Inventory.query.filter_by(product_id=p.id, location_id=l.id).first()
            if existing:
                existing.quantity = qty
            else:
                db.session.add(Inventory(product_id=p.id, location_id=l.id, quantity=qty))
        db.session.commit()
        print('✔ Inventory seeded')

        # ── STOCK MOVES ────────────────────────────────────────
        if StockMove.query.count() > 0:
            print('⚠ Stock moves already exist, skipping')
            return

        moves_data = [
            # ref, type, contact, from_loc, to_loc, date, status, lines[(code,qty),...]
            ('WH/IN/00001','receipt','Azure Interior',None,'WH/Stock-A','2026-02-10','done',
             [('DESK001',20),('CHAIR001',50)]),
            ('WH/IN/00002','receipt','Steel Craft Supplies',None,'WH/Stock-B','2026-02-15','done',
             [('CAB001',15),('SHELF001',30)]),
            ('WH/IN/00003','receipt','TimberWorks India',None,'ND/Shelf-1','2026-02-20','done',
             [('TABLE001',10),('CHAIR002',40),('KEY001',25)]),
            ('WH/IN/00004','receipt','Nova Electronics',None,'WH/Stock-A','2026-03-01','done',
             [('MON001',30),('CABLE01',100)]),
            ('WH/IN/00005','receipt','PackRight Solutions',None,'ND/Shelf-2','2026-03-05','done',
             [('PAPER01',200),('TONER01',20)]),
            ('WH/IN/00006','receipt','Azure Interior',None,'WH/Stock-A','2026-03-16','ready',
             [('DESK001',25),('LAMP001',40)]),
            ('WH/IN/00007','receipt','TimberWorks India',None,'SH/Bay-A','2026-03-18','ready',
             [('CHAIR001',30),('WHTBRD01',15)]),
            ('WH/IN/00008','receipt','Steel Craft Supplies',None,'ND/Shelf-1','2026-03-20','draft',
             [('SHELF001',20),('LOCK001',50)]),
            ('WH/IN/00009','receipt','PackRight Solutions',None,'WH/Stock-B','2026-03-10','ready',
             [('CHAIR002',60),('KEY001',30)]),
            ('WH/IN/00010','receipt','Nova Electronics',None,'SH/Bay-B','2026-03-12','draft',
             [('PROJ001',10),('MON001',15)]),
            ('WH/IN/00011','receipt','Azure Interior',None,'WH/Stock-A','2026-03-17','waiting',
             [('TABLE001',12),('DESK001',8)]),
            ('WH/OUT/00001','delivery','Pinnacle Furnishings','WH/Stock-A',None,'2026-02-12','done',
             [('DESK001',10),('CHAIR001',20)]),
            ('WH/OUT/00002','delivery','Metro Office Hub','WH/Stock-A',None,'2026-02-18','done',
             [('MON001',15),('KEY001',40)]),
            ('WH/OUT/00003','delivery','GreenLeaf Interiors','ND/Shelf-1',None,'2026-02-25','done',
             [('TABLE001',5),('SHELF001',10)]),
            ('WH/OUT/00004','delivery','Skyline Commercial','SH/Bay-A',None,'2026-03-03','done',
             [('CHAIR002',25),('LOCK001',15)]),
            ('WH/OUT/00005','delivery','Pinnacle Furnishings','WH/Stock-A',None,'2026-03-15','ready',
             [('DESK001',12),('CHAIR001',35),('LAMP001',10)]),
            ('WH/OUT/00006','delivery','Coastal Retail Group','ND/Shelf-1',None,'2026-03-19','ready',
             [('MON001',20),('CABLE01',50)]),
            ('WH/OUT/00007','delivery','Metro Office Hub','WH/Stock-B',None,'2026-03-11','ready',
             [('CAB001',8),('TONER01',10)]),
            ('WH/OUT/00008','delivery','Skyline Commercial','SH/Bay-A',None,'2026-03-13','draft',
             [('CHAIR002',30),('LOCK001',20)]),
            ('WH/OUT/00009','delivery','GreenLeaf Interiors','WH/Stock-A',None,'2026-03-16','waiting',
             [('DESK001',15),('PROJ001',5)]),
            ('WH/OUT/00010','delivery','Coastal Retail Group','ND/Shelf-2',None,'2026-03-18','waiting',
             [('PAPER01',150),('SHELF001',10)]),
            ('WH/INT/00001','internal',None,'WH/Stock-A','ND/Shelf-1','2026-03-06','done',
             [('CHAIR001',20),('KEY001',15)]),
            ('WH/INT/00002','internal',None,'ND/Shelf-1','SH/Bay-A','2026-03-15','ready',
             [('CHAIR002',30),('CABLE01',40)]),
            ('WH/INT/00003','internal',None,'WH/Stock-A','SH/Bay-B','2026-03-17','draft',
             [('MON001',10),('LAMP001',20)]),
        ]

        for ref, optype, contact_name, from_loc, to_loc, sdate, status, lines in moves_data:
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

            # move history for done operations
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
        print('✔ Stock moves + lines + history seeded')
        print('\n🎉 All seed data inserted successfully!')


if __name__ == '__main__':
    seed()
