# Image Analyzer - تحليل الصور بالبايثون
# يستخرج النص من الصور (OCR) + معلومات الصورة

from PIL import Image
import sys

def analyze_image(path):
    try:
        img = Image.open(path)
        
        print("=" * 50)
        print("       تحليل الصورة - Image Analyzer")
        print("=" * 50)
        
        # معلومات الصورة الأساسية
        print(f"\n📁 الملف: {path}")
        print(f"📐 الحجم: {img.width} x {img.height} pixel")
        print(f"🎨 النوع: {img.mode}")
        print(f"📦 الصيغة: {img.format}")
        
        # محاولة استخراج النص (OCR)
        print("\n" + "=" * 50)
        print("       النص المستخرج:")
        print("=" * 50)
        
        try:
            import pytesseract
            text = pytesseract.image_to_string(img)
            if text.strip():
                print(text)
            else:
                print("(ما في نص بالصورة)")
        except ImportError:
            print("⚠️  pytesseract مو مثبت - نزّله بـ:")
            print("    pip install pytesseract")
            print("    + نزّل Tesseract من: https://github.com/tesseract-ocr/tesseract")
        except Exception as e:
            print(f"⚠️  خطأ بالOCR: {e}")
        
        print("\n" + "=" * 50)
        
    except FileNotFoundError:
        print(f"❌ الملف مو موجود: {path}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_image(sys.argv[1])
    else:
        print("Usage: python image_analyzer.py <path_to_image>")
        print("Example: python image_analyzer.py photo.jpg")
