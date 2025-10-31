from flask import Blueprint, jsonify, render_template
import csv
import re
import os

trend_bp = Blueprint("trend_bp", __name__)

# path ke file CSV (relative dari posisi file ini)
CSV_PATH = os.path.join(os.path.dirname(__file__), "../../model/harga_tbs_monthly_clean.csv")




MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04", "mei": "05", "may": "05", "jun": "06",
    "jul": "07", "agu": "08", "aug": "08", "sep": "09", "okt": "10", "oct": "10", "nov": "11", "des": "12", "dec": "12"
}

DATE_YYYY_MM_RE = re.compile(r"^\s*(\d{4})[-/](\d{1,2})\s*$")      # 2025-01 or 2025/1
DATE_MM_YYYY_RE = re.compile(r"^\s*(\d{1,2})[-/](\d{4})\s*$")      # 01-2025 or 1/2025
DATE_TEXT_RE = re.compile(r"([A-Za-z]+)\s+(\d{4})")               # Jan 2020 or Mei 2020

def _read_csv(file_path: str):
    data = []
    try:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            # debug: lihat header yang terbaca (bisa comment out setelah yakin)
            print("CSV columns:", reader.fieldnames)

            for row_idx, row in enumerate(reader, start=1):
                # ambil kolom2 yang mungkin ada
                raw_date = (row.get("date") or row.get("Date") or row.get("tanggal") or row.get("Tanggal") or "").strip()
                month_col = (row.get("month") or row.get("Month") or "").strip()
                year_col = (row.get("year") or row.get("Year") or row.get("tahun") or row.get("Tahun") or "").strip()
                price_str = (row.get("price") or row.get("Price") or row.get("harga") or row.get("Harga") or "0").replace(",", "").strip()

                # parse price aman
                try:
                    price = float(price_str) if price_str != "" else 0.0
                except ValueError:
                    price = 0.0

                # default placeholders
                parsed_year = None
                parsed_month = None

                # 1) jika ada kolom month & year langsung -> gunakan itu
                if month_col and year_col:
                    parsed_year = year_col
                    # month bisa 'Jan' atau '01' atau 'Januari' -> normalisasi ke '01'..'12' atau 'Jan'
                    mm = month_col.strip()
                    # if numeric like 1 or 01
                    if re.fullmatch(r"\d{1,2}", mm):
                        parsed_month = mm.zfill(2)
                    else:
                        mm3 = mm[:3].lower()
                        if mm3 in MONTH_MAP:
                            parsed_month = MONTH_MAP[mm3]
                        else:
                            # fallback: keep raw truncated
                            parsed_month = mm

                # 2) jika ada raw_date, coba parse berbagai format
                if raw_date:
                    m = DATE_YYYY_MM_RE.match(raw_date)
                    if m:
                        # format 2025-01
                        y, mth = m.group(1), m.group(2).zfill(2)
                        # jika year_col ada dan bertentangan, prioritaskan year_col sebagai sumber kebenaran
                        if year_col and year_col.isdigit():
                            parsed_year = year_col
                            parsed_month = mth
                        else:
                            parsed_year = y
                            parsed_month = mth
                    else:
                        m2 = DATE_MM_YYYY_RE.match(raw_date)
                        if m2:
                            mth, y = m2.group(1).zfill(2), m2.group(2)
                            if year_col and year_col.isdigit():
                                parsed_year = year_col
                                parsed_month = mth
                            else:
                                parsed_year = y
                                parsed_month = mth
                        else:
                            m3 = DATE_TEXT_RE.search(raw_date)
                            if m3:
                                mon_text, y = m3.group(1), m3.group(2)
                                mon3 = mon_text[:3].lower()
                                parsed_year = year_col if (year_col and year_col.isdigit()) else y
                                parsed_month = MONTH_MAP.get(mon3, mon3)

                # 3) jika belum dapat parsed_year tapi ada year_col -> ambil dari year_col
                if (not parsed_year or not str(parsed_year).isdigit()) and year_col and year_col.isdigit():
                    parsed_year = year_col

                # 4) final fallback: kalau masih kosong, isi default supaya tidak null
                if not parsed_year or not str(parsed_year).isdigit():
                    parsed_year = "0"
                if not parsed_month:
                    # default ke "01" jika tidak tahu bulan
                    parsed_month = "01"

                # normalize strings
                parsed_year = str(parsed_year)
                parsed_month = str(parsed_month).zfill(2) if re.fullmatch(r"\d{1,2}", parsed_month) else parsed_month

                # buat date downstream konsisten: format "YYYY-MM"
                date_normal = f"{parsed_year}-{parsed_month}"

                data.append({
                    "raw_date": raw_date,
                    "month": parsed_month,   # '01'..'12' atau text fallback
                    "year": int(parsed_year) if parsed_year.isdigit() else 0,
                    "date": date_normal,
                    "price": price,
                    "_row_idx": row_idx
                })

    except Exception as e:
        print("CSV read error:", e)
    return data




@trend_bp.route("/api/palm-oil")
def get_palm_oil():
    try:
        data = _read_csv(CSV_PATH)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@trend_bp.route("/trend-pasar")
def trend_pasar_page():
    data = _read_csv(CSV_PATH)
    return render_template("trend_pasar.html", data=data)