### -*- coding: utf-8 -*- ####################################################

from django import template
register = template.Library()

toast_str = "$().toastmessage('%(type)s', '%(message)s');"

js_onload = """<script type="text/javascript">//<![CDATA[
  $(window).load(function(){
    %s
  });
//]]></script>"""


@register.simple_tag()
def toast_message(message, type="success", script_wrap=True):
    """
    Template tag for displaying toast messages
    Example:
    {% toast_message "Hello world" "notice" %}
    Type can be "success", "notice", "warning" or "error"
    You can use tag inside <script> ... </script> with script_wrap=False
    """
    res = toast_str % { 'message': message, 'type': 'show%sToast' % type.capitalize() }
    if script_wrap:
        res = js_onload % res
    return res