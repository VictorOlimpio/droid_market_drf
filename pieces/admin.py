from django.contrib import admin
from pieces.models import Piece

class PieceAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'value']
    list_filter = ('type', 'value')

admin.site.register(Piece, PieceAdmin)