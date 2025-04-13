from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO

def generate_invoice_pdf(commande, facture):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titre
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Facture de Commande")

    # Informations de la facture
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"Numéro de commande : {commande.id}")
    p.drawString(100, height - 100, f"Date : {facture.date.strftime('%d/%m/%Y')}")
    p.drawString(100, height - 120, f"Client : {facture.utilisateur.prenom} {facture.utilisateur.nom}")
    p.drawString(100, height - 140, f"Email : {facture.utilisateur.email}")
    p.drawString(100, height - 160, f"Adresse : {facture.utilisateur.adresse}, {facture.utilisateur.ville}")

    # Détails des articles
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 200, "Détails de la commande")
    p.setFont("Helvetica", 10)

    y = height - 220
    cart_subtotal = 0
    for item in commande.items.all():
        item_total = item.produit.prix * item.quantite
        cart_subtotal += item_total
        p.drawString(100, y, f"{item.produit.nom} x {item.quantite}")
        p.drawString(400, y, f"{item_total} FCFA")
        y -= 20

    # Totaux
    shipping_cost = 1500  # Doit correspondre à ta logique
    order_total = cart_subtotal + shipping_cost

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y - 20, "Sous-total :")
    p.drawString(400, y - 20, f"{cart_subtotal} FCFA")
    p.drawString(100, y - 40, "Frais de livraison :")
    p.drawString(400, y - 40, f"{shipping_cost} FCFA")
    p.drawString(100, y - 60, "Total :")
    p.drawString(400, y - 60, f"{order_total} FCFA")

    # Statut de paiement
    p.drawString(100, y - 80, f"Statut : {facture.get_statut_display() if hasattr(facture, 'get_statut_display') else facture.statut}")

    # Pied de page
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(100, 50, "Merci pour votre achat !")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer