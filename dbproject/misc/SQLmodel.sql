# Title: Fall 2015 CIS4301 Project checkpoint 1
# Authors: Dax Gerts and Noah Presser
# Date: 13 November 2015
# Description: Schema definition for django web store database

BEGIN;
CREATE TABLE "webstore_contains" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer NOT NULL);
CREATE TABLE "webstore_order" ("order_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order_date" date NOT NULL, "order_paid" integer NOT NULL);
CREATE TABLE "webstore_product" ("product_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "product_name" varchar(50) NOT NULL, "product_description" varchar(200) NOT NULL, "product_price" integer NOT NULL, "product_active" bool NOT NULL, "product_stock_quantity" integer NOT NULL, "contains_id" integer NOT NULL REFERENCES "webstore_contains" ("id"), "order_id" integer NOT NULL REFERENCES "webstore_order" ("order_id"));
CREATE TABLE "webstore_supplier" ("supplier_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "supplier_name" varchar(50) NOT NULL);
CREATE TABLE "webstore_user" ("user_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_name" varchar(50) NOT NULL, "user_password" varchar(50) NOT NULL, "user_address" varchar(50) NOT NULL, "user_email" varchar(50) NOT NULL, "user_is_staff" bool NOT NULL);
CREATE TABLE "webstore_product__new" ("product_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "product_name" varchar(50) NOT NULL, "product_description" varchar(200) NOT NULL, "product_price" integer NOT NULL, "product_active" bool NOT NULL, "product_stock_quantity" integer NOT NULL, "contains_id" integer NOT NULL REFERENCES "webstore_contains" ("id"), "order_id" integer NOT NULL REFERENCES "webstore_order" ("order_id"), "supplys_id" integer NOT NULL REFERENCES "webstore_supplier" ("supplier_id"));
INSERT INTO "webstore_product__new" ("product_active", "supplys_id", "product_id", "order_id", "product_description", "contains_id", "product_stock_quantity", "product_price", "product_name") SELECT "product_active", NULL, "product_id", "order_id", "product_description", "contains_id", "product_stock_quantity", "product_price", "product_name" FROM "webstore_product";
DROP TABLE "webstore_product";
ALTER TABLE "webstore_product__new" RENAME TO "webstore_product";
CREATE INDEX "webstore_product_b9415446" ON "webstore_product" ("contains_id");
CREATE INDEX "webstore_product_69dfcb07" ON "webstore_product" ("order_id");
CREATE INDEX "webstore_product_db682daf" ON "webstore_product" ("supplys_id");
CREATE TABLE "webstore_order__new" ("order_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "order_date" date NOT NULL, "order_paid" integer NOT NULL, "orders_id" integer NOT NULL REFERENCES "webstore_user" ("user_id"));
INSERT INTO "webstore_order__new" ("order_id", "order_date", "orders_id", "order_paid") SELECT "order_id", "order_date", NULL, "order_paid" FROM "webstore_order";
DROP TABLE "webstore_order";
ALTER TABLE "webstore_order__new" RENAME TO "webstore_order";
CREATE INDEX "webstore_order_ecd57eb9" ON "webstore_order" ("orders_id");
CREATE TABLE "webstore_contains__new" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer NOT NULL);
INSERT INTO "webstore_contains__new" ("id", "quantity") SELECT "id", "quantity" FROM "webstore_contains";
DROP TABLE "webstore_contains";
ALTER TABLE "webstore_contains__new" RENAME TO "webstore_contains";

COMMIT;
