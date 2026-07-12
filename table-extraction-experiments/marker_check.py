from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

PDF_PATH = "/home/advait/expense-tracker/statement_unlocked.pdf"


text, _, _ = text_from_rendered(
    PdfConverter(create_model_dict())(PDF_PATH)
)