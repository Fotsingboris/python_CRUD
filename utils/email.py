import logging

from django.core.mail import send_mail, EmailMessage
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)



class EmailUtil(object):
    def __init__(self) -> None:
        logger.info("## EmailUtil ##")
        logger.info(f"Testing mode: {settings.TESTING}")
        self.prod = True if "efficient-research.com" in settings.BASE_URL else False
        logger.info(f"Prod? {self.prod}")
        
        
    def send_generic_email(self, subject: str, content: str, to: str, _from: str = None) -> None:
        logger.info("## Sending generic email ##")
        img_base_src = settings.STATIC_BASE_URL
        
        if not self.prod:
            subject = "{TEST} " + subject
            
        if settings.TESTING:
            logger.info("*** EMAIL TESTING MODE ***")
            logger.info(
                f"Content: {content}\nSubject: {subject}\nSent to: {to}\nFrom:{settings.SITE['_title']}"
            )
        else:
            try:
                logger.info(f"Email subject: {subject}")

                # Using Django's send_mail
                # send_mail(
                #     subject,
                #     content,
                #     _from or f"efficient-research.com <{settings.ADMIN_EMAIL}>",
                #     [to],
                #     fail_silently=False,
                #     html_message=content,
                # )

                #Alternatively, using EmailMessage
                
                email = EmailMessage(
                    subject,
                    content,
                    _from or f"efficient-research.com <{settings.ADMIN_EMAIL}>",
                    [to],
                )
                email.content_subtype = "html"
                email.send()

                logger.info("Generic email sent successfully.")
                
            except Exception as e:
                logger.error(f"Exception: {e}")    
                
#USE THIS AS AN EXAMPLE
# def send_newly_created_user_by_admin(self, user: User, base_url: str = None, password:str=None) -> None:
#     """Send invitation email to supervisor."""
#     logger.info("## Sending Email to Newly Created User By Admin ##")

#     if base_url is None:
#         base_url = settings.BASE_URL

#     body = render_to_string(
#         "emails/account/new_user_by_admin.html",
#         context={
#             "full_name": user.get_full_name(),
#             "base_url": base_url,
#             "email_title": _(f"Welcome on Efficient Research"),
#             'password': password,
#         },
#     )
#     try:
#         self.send_generic_email(
#             subject=_("Account Successfully Created"),
#             content=body,
#             to=user.email,
#         )
#     except Exception as e:
#         logger.info(f"An error occurred: {e}")

