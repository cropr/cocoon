### Payment request for registration to Cocoon 2025

### Registration

| Description | Quantity | Unit | Total |
| :---------- | :------: | ---: | ----: |

{% for d in details %}
| {{ d.description }} | {{ d.quantity or "" }} | {{ d. unitprice + " €" if d.unitprice }} | {{ d.totalprice }} € |
{% endfor %}

### Payment

Please transfer the amount of {{ totalprice }} € to the account of KOSK Cocoon
BE43 3632 4366 9801 with the structured communication {{ paymessage }} within 7 days.

If you would like an invoice in the name of a VAT payer, please contact us at cocoon@kosk.be
stating the VAT details of the party concerned:

- name
- address
- e-mail
- VAT number

Yours sincerely

_The KOSK Cocoon team_
