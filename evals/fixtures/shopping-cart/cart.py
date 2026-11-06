def cart_total(items, discount_percent=0):
    t = 0
    for i in items:
        t = t + i["price"] * i["quantity"]
    t = t - t * discount_percent / 100
    return round(t, 2)
