# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import datetime
from typing import Dict, Optional
from .quiz import Image


MANIFEST_START = '''\
<?xml version="1.0" encoding="UTF-8"?>
<manifest identifier="{manifest_identifier}"
xmlns="http://www.imsglobal.org/xsd/imscp_v1p1"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xsi:schemaLocation="http://www.imsglobal.org/xsd/imscp_v1p1
http://www.imsglobal.org/xsd/qti/qtiv2p1/qtiv2p1_imscpv1p2_v1p0.xsd
http://ltsc.ieee.org/xsd/LOM 
http://www.imsglobal.org/xsd/imsmd_loose_v1p3p2.xsd                       
http://www.imsglobal.org/xsd/imsqti_metadata_v2p1
http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_metadata_v2p1p1.xsd">
  <metadata>
    <schema>QTIv2.1 Package</schema>
    <schemaversion>1.0.0</schemaversion>
        <lom xmlns="http://ltsc.ieee.org/xsd/LOM">
      <educational>
        <learningResourceType>
          <source>QTIv2.1</source>
          <value>QTI Package</value>
        </learningResourceType>
      </educational>
      <general>
        <identifier>
          <entry>Manifest_{manifest_identifier}</entry>
        </identifier>
        <title>
          <string>Quiz</string>
        </title>
      </general>
      <lifeCycle>
        <contribute />
        <version>
          <string>Final 1.0</string>
        </version>
      </lifeCycle>
      <rights>
        <copyrightAndOtherRestrictions>
          <source>LOMv1.0</source>
          <value>yes</value>
        </copyrightAndOtherRestrictions>
        <description>
          <string>2013 IMS Global Learning Consortium Inc.</string>
        </description>
      </rights>
    </lom>
  </metadata>
  <organizations/>
  <resources>
    <resource identifier="{assessment_identifier}" type="imsqti_test_xmlv2p1">
      <file href="{assessment_identifier}/{assessment_identifier}.xml"/>
    </resource>
'''

IMAGE = '''\
    <resource identifier="text2qti_image_{ident}" type="webcontent" href="{path}">
      <file href="{path}"/>
    </resource>
'''

MANIFEST_END = '''\
  </resources>
</manifest>
'''


def imsmanifest(*,
                manifest_identifier: str,
                assessment_identifier: str,
                dependency_identifier: str,
                images: Dict[str, Image],
                date: Optional[str]=None) -> str:
    '''
    Generate `imsmanifest.xml`.
    '''
    if date is None:
        date = str(datetime.date.today())
    xml = []
    xml.append(MANIFEST_START.format(manifest_identifier=manifest_identifier,
                                     assessment_identifier=assessment_identifier,
                                     dependency_identifier=dependency_identifier,
                                     date=date))
    for image in images.values():
        xml.append(IMAGE.format(ident=image.id, path=image.qti_xml_path))
    xml.append(MANIFEST_END)
    return ''.join(xml)
