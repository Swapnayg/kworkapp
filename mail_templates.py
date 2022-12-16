
class MailTemplates():

  def order_mail_receipt_buyer(buyer_username,seller_username,order_qty,order_duration,order_amount,order_number,gig_title):
      mail_content = """<table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #E8F2E8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py o_sans o_text o_text-secondary" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 16px;padding-bottom: 16px;"><table cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_sans o_text o_text-secondary o_b-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;color: #424651;border: 2px solid #2E5DC5;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                    </tr>
                    <tr>
                      <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                    </tr>
                  </tbody>
                </table>
                  <h4 class="o_heading o_text-dark o_mb-xs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 8px;color: #242b3d;font-size: 18px;line-height: 23px;">Hello, """+str(buyer_username).title()+"""</h4>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">Thank you for ordering from Letworkbedone.</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-success o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(buyer_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">View Order Details</a></td>
                      </tr>
                    </tbody>
                  </table>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><!-- hero-white -->


  <div class="o_bg-light o_px-xs" align="center">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
      <tbody>
        <tr>
          <td class="o_bg-white o_sans o_text-xs o_text-light o_px-md o_pt-xs" align="center">
            <p><br data-mce-bogus="1"></p><h4 class="o_heading o_text-dark selected-element" data-color="Dark" data-size="Heading 4" data-min="10" data-max="26">Order Summary</h4><p></p>
            <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td class="o_re o_bb-light" style="font-size: 8px; line-height: 8px; height: 8px;">  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>


  <div class="o_bg-light o_px-xs" align="center">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
      <tbody>
        <tr>
          <td class="o_re o_bg-white o_px o_pt" align="center">

            <div class="o_col o_col-3 o_col-full" style="margin-top:25px; margin-bottom: 25px;">
              <div class="o_px-xs o_sans o_text o_text-light o_left o_xs-center">
                <h4 class="o_heading o_text-dark"><strong>"""+str(gig_title)+"""</strong></h4>

                <p class="o_text-xs o_mb-xs">
                  Quantity: """+str(order_qty)+"""<br>
                  Duration: """+str(order_duration)+"""<br>
                  Seller: """+str(seller_username)+"""<br>
                  <strong class="selected-element">Amount: </strong>"""+str(order_amount)+"""
                  <br>
                </p>

              </div>
            </div>

          </td>
        </tr>
      </tbody>
    </table>
  </div>"""
      return mail_content

  def order_mail_seller(buyer_username,seller_username,order_qty,order_duration,order_amount,order_number,gig_title):
      mail_content =  """
  <div class="box" align="center">
    <div class="container" style="max-width: 632px;margin: 0 auto;">
      <div class="row bg-green o_sans">
        
        <div class="icon-container">
          <div class="icon bg-white" align="center" style="">
            <img src="https://i.ibb.co/2ghjzv2/logo.png" width: "60%" height="75px">
          </div>
        </div>

        <h2 class="o_heading o_mb-xxs">Congratulations!</h2>

        <p class="o_mb-md">You just made a new sale</p>
      </div>
    </div>
  </div>


  <div class="o_bg-light o_px-xs" align="center">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
      <tbody>
        <tr>
          <td class="o_bg-white o_px-md o_py o_sans o_text o_text-secondary" align="center">
            <h4 class="o_heading o_text-dark o_mb-xs"></h4><h4 class="o_heading o_text-dark o_mb-xs selected-element" data-color="Dark" data-size="Heading 4" data-min="10" data-max="26">Hello, """+str(seller_username)+"""</h4>
            <p class="o_mb-md">You just received an order from """+str(buyer_username)+""". Deliver as soon as possible to release your payment.</p>
            <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td width="300" class="o_btn o_bg-success o_br o_heading o_text" align="center"><a label="Button" class="o_text-white" href="https://letworkbedone.com/user/"""+seller_username+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities">View Order Details</a></td>
                </tr>
              </tbody>
            </table>
            
          </td>
        </tr>
      </tbody>
    </table>
  </div>


  <div class="o_bg-light o_px-xs" align="center">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
      <tbody>
        <tr>
          <td class="o_bg-white o_sans o_text-xs o_text-light o_px-md o_pt-xs" align="center">
            <p><br data-mce-bogus="1"></p><h4 class="o_heading o_text-dark selected-element" data-color="Dark" data-size="Heading 4" data-min="10" data-max="26">Order Summary</h4><p></p>
            <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td class="o_re o_bb-light" style="font-size: 8px; line-height: 8px; height: 8px;">  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>


  <div class="o_bg-light o_px-xs" align="center">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
      <tbody>
        <tr>
          <td class="o_re o_bg-white o_px o_pt" align="center">

            <div class="o_col o_col-3 o_col-full" style="margin-top:25px; margin-bottom: 25px;">
              <div class="o_px-xs o_sans o_text o_text-light o_left o_xs-center">
                <h4 class="o_heading o_text-dark"><strong>"""+ str(gig_title)+"""</strong></h4>

                <p class="o_text-xs o_mb-xs">
                  Quantity: """+ str(order_qty)+"""<br>
                  Duration: """+ str(order_duration)+"""<br>
                  Buyer: """+ str(seller_username)+"""<br>
                  <strong class="selected-element">Amount: </strong>"""+ str(order_amount)+"""
                  <br>
                </p>

              </div>
            </div>

          </td>
        </tr>
      </tbody>
    </table>
  </div>"""
      return mail_content

  def order_delivered(seller_username,del_message,order_number):
      mail_content = """
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-primary o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-white" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #2E5DC5;color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;">
                  <table cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td class="o_sans o_text o_text-secondary o_bg-white o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png"  alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                      <tr>
                        <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;font-size: 30px;line-height: 39px;">Order Delivered</h2>
                <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">Your order has been delivered and is pending approval.</p></td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- order-intro -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py o_sans o_text o_text-secondary" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 16px;padding-bottom: 16px;"><h4 class="o_heading o_text-dark o_mb-xs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 8px;color: #242b3d;font-size: 18px;line-height: 23px;">Hi, """+str(seller_username)+"""</h4>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">"""+str(del_message)+"""</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-success o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(seller_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">View My Order</a></td>
                      </tr>
                    </tbody>
                  </table>
                  <div style="font-size: 28px; line-height: 28px; height: 28px;"> </div>
                  <p class="o_text-xs o_text-light" style="font-size: 14px;line-height: 21px;color: #82899a;margin-top: 0px;margin-bottom: 0px;">Your order is still awaiting approval</p></td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
  <!-- customer-details-plain -->"""
      return mail_content

  def revision_requested(buyer_username,seller_username,order_number):
      mail_content = """
  <!-- message -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-light" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #ffffff;color: #82899a;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;"><table cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_sans o_text o_text-secondary o_b-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;color: #424651;border: 2px solid #2E5DC5;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png"  alt="" style="width:60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                    <tr>
                      <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_text-dark o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;color: #242b3d;font-size: 30px;line-height: 39px;">Revision Requested</h2>
                  <p style="margin-top: 0px;margin-bottom: 0px;">Your client requested a modification</p></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
  </table>

  <!-- order-intro -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py o_sans o_text o_text-secondary" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 16px;padding-bottom: 16px;"><h4 class="o_heading o_text-dark o_mb-xs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 8px;color: #242b3d;font-size: 18px;line-height: 23px;">Dear """+str(seller_username)+""" </h4>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">You just received an revision request from """+str(buyer_username)+""" for your order. </p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-success o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(seller_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">See More Details</a></td>
                      </tr>
                    </tbody>
                  </table>
                  <div style="font-size: 28px; line-height: 28px; height: 28px;"> </div>
                  <p class="o_text-xs o_text-light" style="font-size: 14px;line-height: 21px;color: #82899a;margin-top: 0px;margin-bottom: 0px;">Respond as soon as possible for a great experience</p></td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
  <!-- customer-details-plain -->"""
      return mail_content

  def order_cancelled_seller(seller_username,buyer_username,order_number):
      mail_content = """
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-primary o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-white" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #2E5DC5;color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;">
                  <table cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td class="o_sans o_text o_text-secondary o_bg-white o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="max-width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                      <tr>
                        <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;font-size: 30px;line-height: 39px;">Order Canceled</h2>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">Your Order Has Been Cancelled And All Funds Returned To Buyer.</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-white o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #ffffff;border-radius: 4px;"><a class="o_text-primary" href=https://letworkbedone.com/user/"""+str(seller_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities style="text-decoration: none;outline: none;color: #2E5DC5;display: block;padding: 12px 24px;mso-text-raise: 3px;">View Order Details</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>"""
      return mail_content

  def order_cancelled_buyer(buyer_username,order_number):
      mail_content = """
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-primary o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-white" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #2E5DC5;color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;">
                  <table cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td class="o_sans o_text o_text-secondary o_bg-white o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width:60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                      <tr>
                        <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;font-size: 30px;line-height: 39px;">Order Canceled</h2>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">Your Order Has Been Cancelled And All Funds Returned To Your Shopping Balance.</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-white o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #ffffff;border-radius: 4px;"><a class="o_text-primary" href="https://letworkbedone.com/user/"""+str(buyer_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #2E5DC5;display: block;padding: 12px 24px;mso-text-raise: 3px;">View Order Details</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>"""
      return mail_content

  def order_extension(sender_username,receiver_username,order_number):
      mail_content = """ <table width="100%" cellspacing="0" cellpadding="0" border="0">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #E8F2E8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-light" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #ffffff;color: #82899a;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;">
                  <table cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td class="o_sans o_text o_text-white o_bg-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #2E5DC5;color: #ffffff;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                      <tr>
                        <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_text-dark o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;color: #242b3d;font-size: 30px;line-height: 39px;">Order Extension Request </h2>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">"""+str(sender_username)+""" Has Sent Extension Request To Your Order. </p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-primary o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(receiver_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">View Order</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><!-- hero-white -->"""
      return mail_content

  def order_extension_decline(sender_username,receiver_username,order_number,reason):
      mail_content = """
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #E8F2E8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-light" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #ffffff;color: #82899a;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;"><table cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_sans o_text o_text-white o_bg-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #2E5DC5;color: #ffffff;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                    </tr>
                    <tr>
                      <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                    </tr>
                  </tbody>
                </table>
                  <h2 class="o_heading o_text-dark o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;color: #242b3d;font-size: 30px;line-height: 39px;">Extension Declined </h2>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">We are sorry for the inconvenience, but your Extension was declined because """+str(reason)+""". Please correct and """+str(sender_username)+""", have an conversation and come to one point.</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-primary o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(receiver_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">See More Details</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><!-- hero-white -->"""
      return mail_content

  def order_extension_accepted(sender_username,receiver_username,order_number):
      mail_content = """
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #E8F2E8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-light" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #ffffff;color: #82899a;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;"><table cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_sans o_text o_text-white o_bg-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #2E5DC5;color: #ffffff;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                    </tr>
                    <tr>
                      <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                    </tr>
                  </tbody>
                </table>
                  <h2 class="o_heading o_text-dark o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;color: #242b3d;font-size: 30px;line-height: 39px;">Extension Approved </h2>
                  <p class="o_mb-md" style="margin-top: 0px;margin-bottom: 24px;">Congratulations, your request has been approved by the """+ str(sender_username)+ """.</p>
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-primary o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(receiver_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">See More Details</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><!-- hero-white -->"""
      return mail_content

  def order_tip_received(buyer_username,gig_title,gig_category,seller_username,order_number,):
      mail_content = """
  <!-- message -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xl o_xs-py-md o_sans o_text-md o_text-light" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;background-color: #ffffff;color: #82899a;padding-left: 24px;padding-right: 24px;padding-top: 64px;padding-bottom: 64px;"><table cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_sans o_text o_text-secondary o_b-primary o_px o_py o_br-max" align="center" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;color: #424651;border: 2px solid #2E5DC5;border-radius: 96px;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><img src="https://i.ibb.co/2ghjzv2/logo.png" alt="" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;"></td>
                      </tr>
                    <tr>
                      <td style="font-size: 24px; line-height: 24px; height: 24px;"> </td>
                      </tr>
                    </tbody>
                  </table>
                  <h2 class="o_heading o_text-dark o_mb-xxs" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 4px;color: #242b3d;font-size: 30px;line-height: 39px;">Tip Received</h2>
                  <p style="margin-top: 0px;margin-bottom: 0px;">You just received an tip from the """+str(buyer_username)+"""</p></td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
  </table>

  <!-- service-primary -->
    <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-md o_sans o_text o_text-secondary" align="left" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 24px;padding-bottom: 24px;">
                <p class="o_text-xxs o_text-light o_mb" style="font-size: 14px;line-height: 19px;color: #82899a;margin-top: 0px;margin-bottom: 16px;">Details of the proposal created</p>
                <h6 class="o_heading o_text-dark" style="font-family: Helvetica, Arial, sans-serif;font-size: 12px;font-weight: bold;margin-top: 0px;margin-bottom: 2px;color: #242b3d;font-size: 24px;line-height: 25px;">Gig Title: """+ str(gig_title)+"""</h6>
                  
                  <p class="o_mb" style="margin-top: 0px;font-size: 14px;margin-bottom: 2px;"><strong>Category:</strong> """+ gig_category+""" <br>
                  </p>
                  <p style="margin-top: 0px;margin-bottom: 0px;font-size: 14px;"><strong>Buyer:</strong>"""+ str(buyer_username)+"""<br>
                  </p>

                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
  <!-- service-light -->

  <!-- button-success -->
  <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
    <tbody>
      <tr>
        <td class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
          <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
            <tbody>
              <tr>
                <td class="o_bg-white o_px-md o_py-xs" align="center" style="background-color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 8px;padding-bottom: 8px;">
                  <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                    <tbody>
                      <tr>
                        <td width="300" class="o_btn o_bg-success o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;"><a class="o_text-white" href="https://letworkbedone.com/user/"""+str(seller_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">View All Proposals</a></td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
  <!-- button-dark -->
  """
      return mail_content

  def chat_message(sender_username,receiver_username,message,message_date):
      mail_content = """
  <!-- subtitle -->
  <div class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px-md o_pt" align="center" style="background-color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 16px;"><h4 class="o_heading o_text-dark" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;color: #242b3d;font-size: 18px;line-height: 23px;">You have a message</h4>
            <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td width="140" class="o_bb-light" style="font-size: 8px;line-height: 8px;height: 8px;border-bottom: 1px solid #d3dce0;">  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- discount_title -->
    
  <!-- message -->
  <div class="o_bg-light o_px-xs" align="left" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px-md o_py-md o_sans o_text o_text-secondary" align="left" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 24px;padding-bottom: 24px;">
            <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td width="48" class="o_bb-light o_text-md o_text-secondary o_sans o_py" align="right" style="vertical-align: top;font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;color: #424651;border-bottom: 1px solid #d3dce0;padding-top: 16px;padding-bottom: 16px;">
                    <img class="o_br-max" src="https://i.ibb.co/2ghjzv2/logo.png" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;border-radius: 96px;">
                  </td>
                  <td class="o_bb-light o_text o_text-secondary o_sans o_px o_py" align="left" style="vertical-align: top;font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;color: #424651;border-bottom: 1px solid #d3dce0;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><p style="margin-top: 0px;margin-bottom: 0px;"><strong class="o_text-dark" style="color: #242b3d;">"""+ str(sender_username) +"""</strong> <span class="o_text-default o_text-xs" style="font-size: 14px;line-height: 21px;"> <span class="o_text-light" style="color: #82899a;"> ●</span> Sender</span></p>
                  <p class="o_text-xxs o_text-light" style="font-size: 12px;line-height: 19px;color: #82899a;margin-top: 0px;margin-bottom: 0px;">"""+ str(message_date) +"""</p>

                </td>
                </tr>
              </tbody>
            </table>
            <div style="font-size: 24px; line-height: 24px; height: 24px;">  </div>
            <p class="o_mb-xs" style="margin-top: 0px;margin-bottom: 8px;"><strong>Message:</strong></p>
            <p class="o_mb-xs" style="margin-top: 0px;margin-bottom: 8px;">"""+ str(message)+""" </p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- message_images -->

  <!-- buttons -->
  <div class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px o_pb-md" align="center" style="background-color: #ffffff;padding-left: 16px;padding-right: 16px;padding-bottom: 24px;">
            <div class="o_col_i" style="display: inline-block;vertical-align: top;">
              <div style="font-size: 24px; line-height: 24px; height: 24px;">  </div>
              <div class="o_px-xs" style="padding-left: 8px;padding-right: 8px;">
                <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_btn o_bg-primary o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;">
                        <a class="o_text-white" href="https://letworkbedone.com/inbox/"""+str(receiver_username)+"""" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">Reply to Message</a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  """
      return mail_content
    
  def chat_order_message(sender_username,receiver_username,message,message_date,order_number):
    mail_content = """
  <!-- subtitle -->
  <div class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px-md o_pt" align="center" style="background-color: #ffffff;padding-left: 24px;padding-right: 24px;padding-top: 16px;"><h4 class="o_heading o_text-dark" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;color: #242b3d;font-size: 18px;line-height: 23px;">You have a message</h4>
            <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td width="140" class="o_bb-light" style="font-size: 8px;line-height: 8px;height: 8px;border-bottom: 1px solid #d3dce0;">  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- discount_title -->
    
  <!-- message -->
  <div class="o_bg-light o_px-xs" align="left" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px-md o_py-md o_sans o_text o_text-secondary" align="left" style="font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;background-color: #ffffff;color: #424651;padding-left: 24px;padding-right: 24px;padding-top: 24px;padding-bottom: 24px;">
            <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation">
              <tbody>
                <tr>
                  <td width="48" class="o_bb-light o_text-md o_text-secondary o_sans o_py" align="right" style="vertical-align: top;font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 19px;line-height: 28px;color: #424651;border-bottom: 1px solid #d3dce0;padding-top: 16px;padding-bottom: 16px;">
                    <img class="o_br-max" src="https://i.ibb.co/2ghjzv2/logo.png" style="width: 60%;-ms-interpolation-mode: bicubic;vertical-align: middle;border: 0;line-height: 100%;height: auto;outline: none;text-decoration: none;border-radius: 96px;">
                  </td>
                  <td class="o_bb-light o_text o_text-secondary o_sans o_px o_py" align="left" style="vertical-align: top;font-family: Helvetica, Arial, sans-serif;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;color: #424651;border-bottom: 1px solid #d3dce0;padding-left: 16px;padding-right: 16px;padding-top: 16px;padding-bottom: 16px;"><p style="margin-top: 0px;margin-bottom: 0px;"><strong class="o_text-dark" style="color: #242b3d;">"""+ sender_username +"""</strong> <span class="o_text-default o_text-xs" style="font-size: 14px;line-height: 21px;"> <span class="o_text-light" style="color: #82899a;"> ●</span> Sender</span></p>
                  <p class="o_text-xxs o_text-light" style="font-size: 12px;line-height: 19px;color: #82899a;margin-top: 0px;margin-bottom: 0px;">"""+ str(message_date) +"""</p>

                </td>
                </tr>
              </tbody>
            </table>
            <div style="font-size: 24px; line-height: 24px; height: 24px;">  </div>
            <p class="o_mb-xs" style="margin-top: 0px;margin-bottom: 8px;"><strong>Message:</strong></p>
            <p class="o_mb-xs" style="margin-top: 0px;margin-bottom: 8px;">"""+ str(message) +""" </p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <!-- message_images -->

  <!-- buttons -->
  <div class="o_bg-light o_px-xs" align="center" style="background-color: #e8f2e8;padding-left: 8px;padding-right: 8px;">
    <table class="o_block" width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation" style="max-width: 632px;margin: 0 auto;">
      <tbody>
        <tr>
          <td class="o_bg-white o_px o_pb-md" align="center" style="background-color: #ffffff;padding-left: 16px;padding-right: 16px;padding-bottom: 24px;">
            <div class="o_col_i" style="display: inline-block;vertical-align: top;">
              <div style="font-size: 24px; line-height: 24px; height: 24px;">  </div>
              <div class="o_px-xs" style="padding-left: 8px;padding-right: 8px;">
                <table align="center" cellspacing="0" cellpadding="0" border="0" role="presentation">
                  <tbody>
                    <tr>
                      <td class="o_btn o_bg-primary o_br o_heading o_text" align="center" style="font-family: Helvetica, Arial, sans-serif;font-weight: bold;margin-top: 0px;margin-bottom: 0px;font-size: 16px;line-height: 24px;mso-padding-alt: 12px 24px;background-color: #2E5DC5;border-radius: 4px;">
                        <a class="o_text-white" href="https://letworkbedone.com/user/"""+str(receiver_username)+"""/manage_orders/"""+str(order_number).replace("#","")+"""/activities" style="text-decoration: none;outline: none;color: #ffffff;display: block;padding: 12px 24px;mso-text-raise: 3px;">Reply to Message</a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  """
    
    return mail_content