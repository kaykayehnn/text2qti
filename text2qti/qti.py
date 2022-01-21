# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import io
import pathlib
import re
import os
import html
from typing import Union, BinaryIO
import zipfile

from .quiz import Quiz
from .markdown import Markdown
from .xml_imsmanifest import imsmanifest
from .xml_assessment_meta import assessment_meta
from .xml_assessment import assessment

# Escape escaped dollars, so they keep their escaping
DOLLAR = '@@DOLLAR@@'

class QTI(object):
    '''
    Create QTI from a Quiz object.
    '''
    def __init__(self, quiz: Quiz, dropDownQuestions = None, equationQuestions = None, config = None):
        self.quiz = quiz
        id_base = 'text2qti'
        self.manifest_identifier = f'{id_base}_manifest_{quiz.id}'
        self.assessment_identifier = f'{id_base}_assessment_{quiz.id}'
        self.dependency_identifier = f'{id_base}_dependency_{quiz.id}'
        self.assignment_identifier = f'{id_base}_assignment_{quiz.id}'
        self.assignment_group_identifier = f'{id_base}_assignment-group_{quiz.id}'

        # Assessment and questions must be generated before imsmanifest because
        # it depends on the item paths.
        self.assessment = (html.unescape(
                          assessment(quiz=quiz,
                                     assessment_identifier=self.assessment_identifier,
                                     title_xml=quiz.title_xml)))


        self.doDropdownQuestions(dropDownQuestions)
        self.doEquationQuestions(equationQuestions)
        self.postprocess(config)
        self.questions = self.parseQuestionsAndUpdateAssessment()

        self.imsmanifest_xml = imsmanifest(manifest_identifier=self.manifest_identifier,
                                           assessment_identifier=self.assessment_identifier,
                                           dependency_identifier=self.dependency_identifier,
                                           images=self.quiz.images, questions=self.questions)
        self.assessment_meta = assessment_meta(assessment_identifier=self.assessment_identifier,
                                               assignment_identifier=self.assignment_identifier,
                                               assignment_group_identifier=self.assignment_group_identifier,
                                               title_xml=quiz.title_xml,
                                               description_html_xml=quiz.description_html_xml,
                                               points_possible=quiz.points_possible,
                                               shuffle_answers=quiz.shuffle_answers_xml,
                                               show_correct_answers=quiz.show_correct_answers_xml,
                                               one_question_at_a_time=quiz.one_question_at_a_time_xml,
                                               cant_go_back=quiz.cant_go_back_xml)


    def write(self, bytes_stream: BinaryIO):
        with zipfile.ZipFile(bytes_stream, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('imsmanifest.xml', self.imsmanifest_xml)
            zf.writestr(zipfile.ZipInfo('non_cc_assessments/'), b'')
            zf.writestr(f'{self.assessment_identifier}/{self.assessment_identifier}.xml', self.assessment)
            for (id, path,question) in self.questions:
                zf.writestr(path, question)
            for image in self.quiz.images.values():
                zf.writestr(image.qti_zip_path, image.data)

    def postprocess(self, config):
        self.assessment = re.sub(
                f"@@@QUESTION_START@@@[0-9a-f]{{32}}@@@QUESTION_END@@@",
                "",
                self.assessment,
            )
        self.assessment = self.assessment.replace('<br>', '<br/>')
        self.assessment = re.sub(r'style="[^"]+"', "", self.assessment)
        self.assessment = re.sub(r'border="[^"]+"', "", self.assessment)

        images = re.finditer(r"<img[^>]+?>", self.assessment)
        for match in images:
            if match.group(0).find('alt') < 0:
                self.assessment = self.assessment.replace(match.group(0), match.group(0).replace("<img", '<img alt=""'), 1)
        
        self.assessment = (
            self.assessment
            .replace("</inlineChoiceInteraction>]", "</inlineChoiceInteraction>")
            .replace("[<inlineChoiceInteraction", "<inlineChoiceInteraction")
        )


    def zip_bytes(self) -> bytes:
        stream = io.BytesIO()
        self.write(stream)
        return stream.getvalue()
    
    def parseQuestionsAndUpdateAssessment(self):
        questions = []
        newAssessment = self.assessment
        matches = re.findall(r'<assessmentItem[\w\W]+?<\/assessmentItem>', self.assessment)
        for match in matches:
            id = re.search(r'<assessmentItem[\w\W]+?identifier="([\w\W]+?)"', match).group(1)
            question = f'<?xml version="1.0" encoding="utf-8"?>{os.linesep}{match}'
            href = f'Items/{id}.xml'
            questions.append((id,href,question))
            newAssessment = newAssessment.replace(match, f'''\
            <assessmentItemRef identifier="{id}"
                href="../{href}" required="true"
                fixed="true"/>
''')
        
        self.assessment = newAssessment
        return questions

    def doEquationQuestions(self, equationQuestions):
        for (
            id,
            question,
            answersJson,
            correctAnswersJson,
        ) in equationQuestions:
            match = re.search(f'<assessmentItem identifier="[^"]+"[^>]+?title="{id}"[^>]+?>(?:.|\n)+?<\/assessmentItem>', self.assessment)
            if match is None:
                raise Exception("asd")

            declarations = ""
            outcomeDeclarations = ""
            choicesOutput = ""
            scoringOutput = ""

            for i in range(len(answersJson)):
                answers = os.linesep.join(
                    [
                        f"""\
    <value>{value}</value>
"""
                        for value in correctAnswersJson[i]
                    ]
                )

                mappings = os.linesep.join(
                    [
                        f"""\
    <mapEntry mapKey="{value}" mappedValue="1"></mapEntry>
"""
                        for value in correctAnswersJson[i]
                    ]
                ) 
                choicesOutput += f"""
<div>
    {answersJson[i]["prefix"]}<textEntryInteraction responseIdentifier="RESPONSE{i}" expectedLength="15" />{answersJson[i]["suffix"]}
</div>
"""
                declarations += f"""
    <responseDeclaration identifier="RESPONSE{i}" cardinality="single" baseType="identifier">
        <correctResponse>
            {answers}
        </correctResponse>
        <mapping defaultValue="0">
            {mappings}
        </mapping>
    </responseDeclaration>
"""
                outcomeDeclarations += f"""
    <outcomeDeclaration identifier="SCORE{i}" cardinality="single" baseType="float">
        <defaultValue>
            <value>0.0</value>
        </defaultValue>
    </outcomeDeclaration>
"""
                
                scoringOutput += f"""
       <responseCondition>
            <responseIf>
                <match>
                    <variable identifier="RESPONSE{i}"/>
                    <correct identifier="RESPONSE{i}"/>
                </match>
                <setOutcomeValue identifier="SCORE{i}">
                    <baseValue baseType="float">1.0</baseValue>
                </setOutcomeValue>
            </responseIf>
            <responseElse>
                <setOutcomeValue identifier="SCORE{i}">
                    <baseValue baseType="float">0.0</baseValue>
                </setOutcomeValue>
            </responseElse>
        </responseCondition>
    """



            template = f"""
<assessmentItem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
      xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1
      http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p2.xsd"
	  identifier="{id}" title="Question" adaptive="false" timeDependent="false">
	{declarations}
	<outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float"/>
    {outcomeDeclarations}
	<itemBody>
		<div>{question}</div>
        {choicesOutput}
	</itemBody>
	<responseProcessing>
    {scoringOutput}
	</responseProcessing>
</assessmentItem>
"""
            self.assessment = self.assessment.replace(match.group(0), template)

    def doDropdownQuestions(self, dropdownQuestions):
        xml = self.assessment
        for (
        id,
        question,
        answersJson,
        correctAnswersJson,
        solutionVideo,
    ) in dropdownQuestions:
            question = question.replace('<br>', '<br/>').replace("<BR>", "<BR/>")
            question = re.sub(r"(?:response|answer)\s*(\d+)", "DROPDOWN\\1", question, flags=re.IGNORECASE)
            question = re.sub(r"drop\s*?down\s*?", "DROPDOWN", question, flags=re.IGNORECASE)
        # question = question.replace("[DROPDOWN]", "[DROPDOWN1]")
            match = re.search(f'<assessmentItem identifier="[^"]+"[^>]+?title="{id}"[^>]+?>(?:.|\n)+?<\/assessmentItem>', xml)
            if match is None:
                raise Exception("asd")

            declarations = ""
            outcomeDeclarations = ""
            choicesOutput = ""
            scoringOutput = ""

            for i in range(len(answersJson)):
                dropdown = answersJson[i]
                dropdown["text"] = re.sub(r"drop\s*?down\s*?", "DROPDOWN", dropdown["text"], flags=re.IGNORECASE).replace(':', "")
                if len(dropdown["text"]) == 0:
                    dropdown["text"] = f"[DROPDOWN{i}]"

                if question.find(dropdown["text"]) < 0:
                    question += f"{os.linesep}{dropdown['text']}"

                answers = os.linesep.join(
                    [
                        f"""\
    <inlineChoice identifier="text2qti_answer_{id}_{i}_{value["value"]}">
        {value["text"] if value["text"] is not None and len(value["text"]) > 0 else value["image"]}
    </inlineChoice>
"""
                        for value in dropdown["values"]
                    ]
                )
                interaction = f"""\
<inlineChoiceInteraction responseIdentifier="RESPONSE{i}" shuffle="true">
{answers}
</inlineChoiceInteraction>"""
                # Dropdown text most likely contains the question itself
                if len(dropdown["text"]) >= 15:
                    question = question.replace(dropdown["text"], f'{dropdown["text"]}{os.linesep}{interaction}')
                else:
                    question = question.replace(dropdown["text"], interaction)

                declarations += f"""
    <responseDeclaration identifier="RESPONSE{i}" cardinality="single" baseType="identifier">
        <correctResponse>
            <value>text2qti_answer_{id}_{i}_{correctAnswersJson[i]}</value>
        </correctResponse>
    </responseDeclaration>
"""
                outcomeDeclarations += f"""
    <outcomeDeclaration identifier="SCORE{i}" cardinality="single" baseType="float">
        <defaultValue>
            <value>0.0</value>
        </defaultValue>
    </outcomeDeclaration>
"""
                
                scoringOutput += f"""
       <responseCondition>
            <responseIf>
                <match>
                    <variable identifier="RESPONSE{i}"/>
                    <correct identifier="RESPONSE{i}"/>
                </match>
                <setOutcomeValue identifier="SCORE{i}">
                    <baseValue baseType="float">1.0</baseValue>
                </setOutcomeValue>
            </responseIf>
            <responseElse>
                <setOutcomeValue identifier="SCORE{i}">
                    <baseValue baseType="float">0.0</baseValue>
                </setOutcomeValue>
            </responseElse>
        </responseCondition>
    """

            # Dropdown questions should be 1 point for each dropdown, however due
            # to text2qti format this is not possible (see generateQuiz.py)
            template=f"""
<assessmentItem identifier="{id}" title="Question" timeDependent="false"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
      xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1
      http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p2.xsd">
    {declarations}
	<outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float">
        <defaultValue>
            <value>0.0</value>
        </defaultValue>
    </outcomeDeclaration>
    {outcomeDeclarations}
	<itemBody>
		<div>{question}</div>
	</itemBody>
    <responseProcessing>
	{scoringOutput}
    </responseProcessing>
</assessmentItem>
"""
    #         template = f"""
    # <item ident="{id}" title="Question">
    # <itemmetadata>
    #     <qtimetadata>
    #     <qtimetadatafield>
    #     <fieldlabel>question_type</fieldlabel>
    #     <fieldentry>multiple_dropdowns_question</fieldentry>
    #     </qtimetadatafield>
    #     <qtimetadatafield>
    #         <fieldlabel>points_possible</fieldlabel>
    #         <fieldentry>1</fieldentry>
    #     </qtimetadatafield>
    #     <qtimetadatafield>
    #         <fieldlabel>original_answer_ids</fieldlabel>
    #         <fieldentry>{",".join([f'text2qti_answer_{id}_{choice}' for choice in choicesFlattenned])}</fieldentry>
    #     </qtimetadatafield>
    # <qtimetadatafield>
    #     <fieldlabel>assessment_question_identifierref</fieldlabel>
    #     <fieldentry>text2qti_question_ref_{id}</fieldentry>
    # </qtimetadatafield>
    #     </qtimetadata>
    # </itemmetadata>
    # <presentation>
    #     <material>
    #     <mattext texttype="text/html">{question}</mattext>
    #     </material>
    #     {choicesOutput}
    # </presentation>
    # <resprocessing>
    #     <outcomes>
    #     <decvar maxvalue="{len(correctAnswersJson)}" minvalue="0" varname="SCORE" vartype="Decimal"/>
    #     </outcomes>
    #     {scoringOutput}
    # </resprocessing>
    # </item>
    # """
            xml = xml.replace(match.group(0), template)
            # if bool(
            #     re.search(r"^drop\s*down\s\d+:$", dropdown["text"], flags=re.IGNORECASE)
            # ):
            #     dropdown["text"] = f"[DROPDOWN{i+1}]"
            # if not bool(
            #     re.search(r"drop\s*down\s*(\d+)", dropdown["text"], flags=re.IGNORECASE)
            # ):
            #     dropdown["text"] += f"[DROPDOWN{i+1}]"
            # if not bool(
            #     re.search(f"drop\\s*down\\s*{i+1}", question, flags=re.IGNORECASE)
            # ):
            #     question += f"{os.linesep}{dropdown['text']}"

            dropdowns = re.finditer(
                r"\[drop\s*down\s*(\d+)]", question, flags=re.IGNORECASE
            )
            for dropdown in dropdowns:
                break
                index = int(dropdown.group(1)) - 1
                # The question has 4 dropdowns but there are only 2 specified in JSON (ID 12819 and 13769)
                if index >= len(answersJson):
                    continue
                formattedDropdown = dropdown.group(0).replace(" ", "")
                question = question.replace(dropdown.group(0), formattedDropdown)
                # if value["image"] != "":
                #     print(value["image"])
                # TODO: value['image']?
                answers = os.linesep.join(
                    [
                        f"""
    <response_label ident="text2qti_answer_{id}_{index}_{value["value"]}">
        <material>
        <mattext texttype="text/plain">{value["text"]}</mattext>
        </material>
    </response_label>
    """
                        for value in answersJson[index]["values"]
                    ]
                )

                choicesOutput += f"""
    <response_lid ident="response_{formattedDropdown[1:-1]}">
    <material>
    <mattext>{formattedDropdown[1:-1]}</mattext>
    </material>
    <render_choice>
    {answers}
    </render_choice>
    </response_lid>
    """
                scoringOutput += f"""
    <respcondition>
    <conditionvar>
        <varequal respident="response_{formattedDropdown[1:-1]}">text2qti_answer_{id}_{index}_{correctAnswersJson[i]}</varequal>
    </conditionvar>
    <setvar varname="SCORE" action="Add">1.00</setvar>
    </respcondition>
    """

    #         template = f"""
    # <item ident="{id}" title="Question">
    # <itemmetadata>
    #     <qtimetadata>
    #     <qtimetadatafield>
    #     <fieldlabel>question_type</fieldlabel>
    #     <fieldentry>multiple_dropdowns_question</fieldentry>
    #     </qtimetadatafield>
    #     <qtimetadatafield>
    #         <fieldlabel>points_possible</fieldlabel>
    #         <fieldentry>{len(correctAnswersJson)}</fieldentry>
    #     </qtimetadatafield>
    #     <qtimetadatafield>
    #         <fieldlabel>original_answer_ids</fieldlabel>
    #         <fieldentry>{",".join([f'text2qti_answer_{id}_{choice}' for choice in choicesFlattenned])}</fieldentry>
    #     </qtimetadatafield>
    # <qtimetadatafield>
    #     <fieldlabel>assessment_question_identifierref</fieldlabel>
    #     <fieldentry>text2qti_question_ref_{id}</fieldentry>
    # </qtimetadatafield>
    #     </qtimetadata>
    # </itemmetadata>
    # <presentation>
    #     <material>
    #     <mattext texttype="text/html">{question}</mattext>
    #     </material>
    #     {choicesOutput}
    # </presentation>
    # <resprocessing>
    #     <outcomes>
    #     <decvar maxvalue="{len(correctAnswersJson)}" minvalue="0" varname="SCORE" vartype="Decimal"/>
    #     </outcomes>
    #     {scoringOutput}
    # </resprocessing>
    # </item>
    # """
            # xml = xml.replace(match.group(0), template)

        self.assessment = xml


    def save(self, qti_path: Union[str, pathlib.Path]):
        if isinstance(qti_path, str):
            qti_path = pathlib.Path(qti_path)
        elif not isinstance(qti_path, pathlib.Path):
            raise TypeError
        qti_path.write_bytes(self.zip_bytes())
