from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

def generate_invoice_pdf(commande, facture):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # En-tête
    p.setFont("Helvetica-Bold", 18)
    p.drawString(200, height - 50, "FACTURE DE COMMANDE")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"N° Commande : {commande.id}")
    p.drawString(50, height - 120, f"Client : {facture.utilisateur.prenom} {facture.utilisateur.nom}")
    p.drawString(50, height - 140, f"Email : {facture.utilisateur.email}")
    p.drawString(50, height - 160, f"Adresse : {facture.utilisateur.adresse}")

    # Détails des produits
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 200, "Détails")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, height - 220, "Produit")
    p.drawString(300, height - 220, "Quantité")
    p.drawString(400, height - 220, "Total")

    y = height - 240
    p.setFont("Helvetica", 10)
    total = 0
    for item in commande.items.all():
        item_total = item.quantite * item.prix_unitaire
        total += item_total
        p.drawString(50, y, item.produit.nom)
        p.drawString(300, y, str(item.quantite))
        p.drawString(400, y, f"{item_total} FCFA")
        y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y - 20, "Sous-total :")
    p.drawString(400, y - 20, f"{total} FCFA")
    p.drawString(50, y - 40, "Frais de livraison :")
    p.drawString(400, y - 40, "1500 FCFA")
    p.drawString(50, y - 60, "Total :")
    p.drawString(400, y - 60, f"{total + 1500} FCFA")

    p.setFont("Helvetica-Oblique", 9)
    p.drawString(50, 40, "Merci pour votre achat.")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
