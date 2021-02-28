from django.contrib import admin

from .models import User, AuctionListing, Bid, Comment, Category, Info

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_item","bid_price", "bidder")

# Register your models here.

admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Info)