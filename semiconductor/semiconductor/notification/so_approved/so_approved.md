<h3>Demand Request Approved</h3>

<p>Demand Request <b>{{ doc.name }}</b> has been approved.</p>

<!-- show last comment if exists -->
{% if comments %}
<p><i>Last comment: {{ comments[-1].comment }} by {{ comments[-1].by }}</i></p>
{% endif %}

<h4>Details</h4>
<ul>
  <li>Requested By: {{ doc.owner }}</li>
  <li>Customer: {{ doc.customer }}</li>
  <li>Status: {{ doc.status }}</li>
</ul>

<h4>Items Approved</h4>
<ul>
  {% for row in doc.items %}
  <li>{{ row.item_code }} – Qty: {{ row.qty }}</li>
  {% endfor %}
</ul>

<p><a href="{{ frappe.utils.get_url_to_form(doc.doctype, doc.name) }}" target="_blank">
👉 View this Demand Request
</a></p>