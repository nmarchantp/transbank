from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from flask import Flask, request, redirect, render_template

CommerceCode = '597055555532'
ApiKeySecret = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
options = WebpayOptions(CommerceCode, ApiKeySecret, IntegrationType.TEST)
transaction = Transaction(options)

app = Flask(__name__)

@app.route('/')
def index():
     return render_template('formulario_pago.html')

app.route('/pagar', methods=['POST'])
def pagar():
    amount = request.form.get('amount')
    
    response = transaction.create(
        buy_order='orden123',
        session_id='sesion12',
        amount=amount,
        return_url='http://localhost:5000/webpay/return'
    )
    
    redirect_url = response.get('url') + '?token_ws=' + response.get('token')
    if redirect_url:
        return redirect(redirect_url)
    else:
        return 'Error: No se pudo obtener la URL de redirección', 500

@app.route('/webpay/return', methods=['GET'])
def transaccion_completa():
    transaction = Transaction()
    
    token_ws = request.args.get('token_ws')
    
    if not token_ws:
        return 'Error: No se encontró el token de la transacción.', 400
    
    result = transaction.commit(token_ws)
    
    if result.get('status') == 'AUTHORIZED':
        return 'Transacción exitosa'
    else:
        return f'Error en la transacción: {result.get("status")}'

if __name__ == '__main__':
    app.run(debug=True)
