import segno


from qrmaster.core.config import Config
from qrmaster.core.state  import State
from qrmaster.utils.utils import log_step


class QR :
  """
  The QR class is responsible for generating QR codes based on various types of input data.
  This class provides methods to build different types of QR code data, such as URLs, emails,
  Wi-Fi information, geographical locations, vCards, MeCards, and EPC (Electronic Product Code).
  It also provides functionality to generate a QR code based on the data.
  """


  root : dict = {}


  def __init__ ( self ) :
    """
    Initializes the QR code generator.

    This method sets up the initial state for the QR code generation, preparing the necessary
    components to build and generate QR codes for various types of data.
    """
    self.root = Config ().get ( "project" )


  @log_step ( "QR::generate" )
  def generate ( self ) :
    """
    Generates the QR code based on the provided data.

    This method triggers the process of generating a QR code using the provided content data.
    It coordinates the building of data and the final generation of the QR code.

    The method will call the necessary data-building functions based on the content type, and
    then generate the corresponding QR code.

    This method is logged to track the QR code generation process.
    """
    data = self.buildData ( self.root.get ( "content", {} ) )
    qr = segno.make ( data, **self.root.get ( "qr", {} ) )
    State ().add_step ( "QR::generate" )
    State ().save ()
    return qr


  @log_step ( "QR::buildData" )
  def buildData ( self, content : dict ) -> str :
    """
    Builds the data to be embedded in the QR code based on the provided content.

    This method takes a dictionary containing the content for the QR code and determines the
    appropriate data format to generate.

    Args:
        content (dict): A dictionary containing the content to be encoded in the QR code.

    Returns:
        str: The data to be embedded in the QR code.
    """
    content_type = content.get ( "type" )
    data = content.get ( "data" )

    if content_type == "url" :
      return self.urlData ( data )

    elif content_type == "email" :
      return self.emailData ( data )

    elif content_type == "wifi" :
      return self.wifiData ( data )

    elif content_type == "geo" :
      return self.geoData ( data )

    elif content_type == "mecard" :
      return self.mecardData ( data )

    elif content_type == "vcard" :
      return self.vcardData ( data )

    elif content_type == "epc" :
      return self.epcData ( data )

    else :
      raise ValueError ( f"Unsupported content type: {content_type}" )


  @log_step ( "QR::urlData" )
  def urlData ( self, data : dict ) -> str :
    """
    Builds data for a URL QR code.

    This method takes a dictionary containing a URL and prepares it for embedding in a QR code.

    Args:
        data (dict): A dictionary containing a URL to be embedded in the QR code.

    Returns:
        str: The URL data to be embedded in the QR code.
    """
    url = data.get ( "url" )
    if not url :
      raise ValueError ( "URL must be provided for type 'url'" )
    return url


  @log_step ( "QR::emailData" )
  def emailData ( self, data : dict ) -> str :
    """
    Builds data for an email QR code.

    This method takes a dictionary containing an email address and prepares it for embedding
    in a QR code.

    Args:
        data (dict): A dictionary containing an email address to be embedded in the QR code.

    Returns:
        str: The email data to be embedded in the QR code.
    """
    to = data.get ( "to" )
    if not to:
      raise ValueError ( "The 'to' field is required for type 'email'." )

    return segno.helpers.make_make_email_data (
        to = to,
        cc = data.get ( "cc", "" ),
        bcc = data.get ( "bcc", "" ),
        subject = data.get ( "subject", "" ),
        body = data.get ( "body", "" )
      )


  @log_step ( "QR::wifiData" )
  def wifiData ( self, data : dict ) -> str :
    """
    Builds data for a Wi-Fi QR code.

    This method takes a dictionary containing Wi-Fi network information and prepares it for
    embedding in a QR code.

    Args:
        data (dict): A dictionary containing Wi-Fi network information (SSID, password, etc.).

    Returns:
        str: The Wi-Fi data to be embedded in the QR code.
    """
    ssid = data.get ( "ssid" )
    if not ssid :
      raise ValueError ( "SSID must be provided for type 'wifi'" )

    return segno.helpers.make_wifi_data (
        ssid = ssid,
        password = data.get ( "password", "" ),
        security = data.get ( "security", "WPA" )
      )


  @log_step ( "QR::geoData" )
  def geoData ( self, data : dict ) -> str :
    """
    Builds data for a geographical location QR code.

    This method takes a dictionary containing latitude and longitude and prepares it for
    embedding in a QR code.

    Args:
        data (dict): A dictionary containing geographical coordinates (latitude, longitude).

    Returns:
        str: The geographical data to be embedded in the QR code.
    """
    lat = data.get ( "lat" )
    lon = data.get ( "lng" )
    if lat is None or lon is None :
      raise ValueError ( "Latitude and longitude must be provided for type 'geo'" )

    return segno.helpers.make_geo_data ( lat, lon )


  @log_step ( "QR::mecardData" )
  def mecardData ( self, data : dict ) -> str :
    """
    Builds data for a MeCard QR code.

    This method takes a dictionary containing MeCard information and prepares it for embedding
    in a QR code.

    Args:
        data (dict): A dictionary containing MeCard data (name, phone number, etc.).

    Returns:
        str: The MeCard data to be embedded in the QR code.
    """
    name = data.get ( "name" )
    if not name :
      raise ValueError ( "Name must be provided for type 'mecard'" )

    return segno.helpers.make_mecard_data (
        name = name,
        reading = data.get ( "reading", "" ),
        email = data.get ( "email", "" ),
        phone = data.get ( "phone", "" ),
        videophone = data.get ( "videophone", "" ),
        memo = data.get ( "memo", "" ),
        nickname = data.get ( "nickname", "" ),
        birthday = data.get ( "birthday", "" ),
        url = data.get ( "url", "" ),
        pobox = data.get ( "pobox", "" ),
        roomno = data.get ( "roomno", "" ),
        houseno = data.get ( "houseno", "" ),
        city = data.get ( "city", "" ),
        prefecture = data.get ( "prefecture", "" ),
        zipcode = data.get ( "zipcode", "" ),
        country = data.get ( "country", "" )
      )


  @log_step ( "QR::vcardData" )
  def vcardData ( self, data : dict ) -> str :
    """
    Builds data for a vCard QR code.

    This method takes a dictionary containing vCard information and prepares it for embedding
    in a QR code.

    Args:
        data (dict): A dictionary containing vCard data (name, phone number, address, etc.).

    Returns:
        str: The vCard data to be embedded in the QR code.
    """
    name = data.get ( "name" )
    displayname = data.get ( "displayname" )

    if not name or not displayname :
      raise ValueError ( "Name and displayname must be provided for type 'vcard'" )

    return segno.helpers.make_vcard_data (
        name = name,
        displayname = displayname,
        email = data.get ( "email", "" ),
        phone = data.get ( "phone", "" ),
        fax = data.get ( "fax", "" ),
        videophone = data.get ( "videophone", "" ),
        memo = data.get ( "memo", "" ),
        nickname = data.get ( "nickname", "" ),
        birthday = data.get ( "birthday", "" ),
        url = data.get ( "url", "" ),
        pobox = data.get ( "pobox", "" ),
        street = data.get ( "street", "" ),
        city = data.get ( "city", "" ),
        region = data.get ( "region", "" ),
        zipcode = data.get ( "zipcode", "" ),
        country = data.get ( "country", "" ),
        org = data.get ( "org", "" ),
        lat = data.get ( "lat", "" ),
        lng = data.get ( "lng", "" ),
        source = data.get ( "source", "" ),
        rev = data.get ( "rev", "" ),
        title = data.get ( "title", "" ),
        photo_uri = data.get ( "photo_uri", "" ),
        cellphone = data.get ( "cellphone", "" ),
        homephone = data.get ( "homephone", "" ),
        workphone = data.get ( "workphone", "" )
      )


  @log_step ( "QR::epcData" )
  def epcData ( self, data : dict ) -> str :
    """
    Builds data for an EPC (Electronic Product Code) QR code.

    This method takes a dictionary containing EPC data and prepares it for embedding in a QR code.

    Args:
        data (dict): A dictionary containing EPC data.

    Returns:
        str: The EPC data to be embedded in the QR code.
    """
    name = data.get ( "name" )
    iban = data.get ( "iban" )
    amount = data.get ( "amount" )
    if not name or not iban or not amount :
      raise ValueError ( "Name, IBAN, and amount must be provided for type 'epc'" )

    return segno.helpers.make_epc_data (
        name = name,
        iban = iban,
        amount = amount,
        text = data.get ( "text", "" ),
        reference = data.get ( "reference", "" ),
        bic = data.get ( "bic", "" ),
        purpose = data.get ( "purpose", "" ),
        encoding = data.get ( "encoding", "" )
      )
