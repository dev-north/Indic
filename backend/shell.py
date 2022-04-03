import hinglish

while True:
    text = input('hinglish > ')
    result, error = hinglish.execute('<stdin>', text)

    if error: print(error.to_string())
    else: print(result)