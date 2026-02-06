 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..b976203bbfe6900ff0cb190c22c87b1b99e99110
--- /dev/null
+++ b/README.md
@@ -0,0 +1,40 @@
+# 1688 → eBay UK Listing Generator
+
+This repo provides a small CLI that turns 1688 product data into a UK-friendly eBay listing description (Markdown or HTML).
+
+## Quick start
+
+```bash
+python3 ebay_uk_listing.py sample_product.json
+```
+
+```bash
+python3 ebay_uk_listing.py sample_product.json --format html
+```
+
+## Input format
+
+Provide a JSON file with the following fields (any are optional, but `title` is recommended):
+
+```json
+{
+  "title": "Portable Mini Fan",
+  "category": "Personal Care",
+  "brand": "OEM",
+  "model": "MF-01",
+  "material": "ABS",
+  "size": "120 x 60 x 45 mm",
+  "color": "White",
+  "weight": "210 g",
+  "features": ["USB rechargeable", "3 speed settings"],
+  "package_contents": ["Fan", "USB cable", "User manual"],
+  "moq": "2 pcs",
+  "price_range": "¥12-18",
+  "images": ["https://example.com/image1.jpg"],
+  "notes": "Confirm CE compliance before listing."
+}
+```
+
+## Sample data
+
+A ready-to-run sample file is included in `sample_product.json`.
 
EOF
)
