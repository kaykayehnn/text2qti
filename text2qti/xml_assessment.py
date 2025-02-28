# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import os
from .quiz import Quiz, Question, GroupStart, GroupEnd, TextRegion


BEFORE_ITEMS = '''\
<?xml version="1.0" encoding="UTF-8"?>
<assessmentTest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1" identifier="test_{assessment_identifier}"
    title="{title}"
    xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1 http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p2.xsd">
  <outcomeDeclaration identifier="TOTAL_SCORE" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_MAXSCORE" cardinality="single" baseType="float">
      <defaultValue>
          <value>1</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_MINSCORE" cardinality="single" baseType="float">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_NUMBERINCORRECT" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_NUMBERCORRECT" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_NUMBERPRESENTED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_NUMBERSELECTED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_NUMBERRESPONDED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_SCORE" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_MAXSCORE" cardinality="single" baseType="float">
      <defaultValue>
          <value>1</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_MINSCORE" cardinality="single" baseType="float">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_NUMBERINCORRECT" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_NUMBERCORRECT" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_NUMBERPRESENTED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="TOTAL_NUMBERSELECTED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <outcomeDeclaration identifier="SECTION_NUMBERRESPONDED" cardinality="single" baseType="integer">
      <defaultValue>
          <value>0</value>
      </defaultValue>
  </outcomeDeclaration>
  <testPart identifier="testPart_{assessment_identifier}" navigationMode="linear" submissionMode="individual">
    <assessmentSection identifier="root_assessmentSection"
      title=""
      required="true"
      visible="false"
      keepTogether="true"
      fixed="false">
'''

AFTER_ITEMS = '''\
    </assessmentSection>
  </testPart>
  <outcomeProcessing>
      <setOutcomeValue identifier="TOTAL_SCORE">
          <sum>
              <testVariables variableIdentifier="SCORE"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_MAXSCORE">
          <sum>
              <outcomeMinimum outcomeIdentifier="SCORE"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_MINSCORE">
          <sum>
              <outcomeMaximum outcomeIdentifier="SCORE"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_NUMBERINCORRECT">
          <numberIncorrect/>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_NUMBERCORRECT">
          <numberCorrect/>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_NUMBERRESPONDED">
          <numberResponded/>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_NUMBERSELECTED">
          <numberSelected/>
      </setOutcomeValue>
      <setOutcomeValue identifier="TOTAL_NUMBERPRESENTED">
          <numberPresented/>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_SCORE">
          <sum>
              <testVariables variableIdentifier="SCORE" sectionIdentifier="{assessment_identifier}"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_MAXSCORE">
          <sum>
              <outcomeMinimum outcomeIdentifier="SCORE" sectionIdentifier="{assessment_identifier}"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_MINSCORE">
          <sum>
              <outcomeMaximum outcomeIdentifier="SCORE" sectionIdentifier="{assessment_identifier}"/>
          </sum>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_NUMBERINCORRECT">
          <numberIncorrect sectionIdentifier="{assessment_identifier}"/>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_NUMBERCORRECT">
          <numberCorrect sectionIdentifier="{assessment_identifier}"/>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_NUMBERRESPONDED">
          <numberResponded sectionIdentifier="{assessment_identifier}"/>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_NUMBERSELECTED">
          <numberSelected sectionIdentifier="{assessment_identifier}"/>
      </setOutcomeValue>
      <setOutcomeValue identifier="SECTION_NUMBERPRESENTED">
          <numberPresented sectionIdentifier="{assessment_identifier}"/>
      </setOutcomeValue>
  </outcomeProcessing>
</assessmentTest>
'''

GROUP_START = '''\
    <assessmentSection identifier="group_{ident}" title="{group_title}" visible="false">
      <selection select="{pick}" />
'''

GROUP_END = '''\
    </assessmentSection>
'''

TEXT = '''\
      <rubricBlock view="author candidate proctor scorer testConstructor tutor">
          {text_html_xml}
      </rubricBlock>
'''

START_ITEM = '''\
      <assessmentItem identifier="question_{question_identifier}"
      title="{question_title}"
      timeDependent="false"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
      xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1
      http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p1.xsd">
'''

END_ITEM = '''\
      </assessmentItem>
'''


ITEM_METADATA_MCTF_SHORTANS_MULTANS_NUM = '''\
'''

ITEM_METADATA_ESSAY = ITEM_METADATA_MCTF_SHORTANS_MULTANS_NUM.replace('{original_answer_ids}', '')

ITEM_METADATA_UPLOAD = ITEM_METADATA_ESSAY

ITEM_PRESENTATION_MCTF = '''\
        <itemBody>
          <div>
          {question_html_xml}
          </div>
          <choiceInteraction responseIdentifier="RESPONSE" shuffle="true">
{choices}
          </choiceInteraction>
        </itemBody>
'''

ITEM_PRESENTATION_MCTF_CHOICE = '''\
              <simpleChoice
                identifier="{ident}"
                fixed="false" showHide="show">
                {choice_html_xml}
              </simpleChoice>'''

ITEM_PRESENTATION_MULTANS = ITEM_PRESENTATION_MCTF.replace('<choiceInteraction', '<choiceInteraction maxChoices="{maxChoices}"')

ITEM_PRESENTATION_MULTANS_CHOICE = ITEM_PRESENTATION_MCTF_CHOICE

ITEM_PRESENTATION_SHORTANS = '''\
        <itemBody>
          <div>
          {question_html_xml}
          <p><textEntryInteraction responseIdentifier="RESPONSE" expectedLength="15" /></p>
          </div>
        </itemBody>
'''

ITEM_PRESENTATION_ESSAY = '''\
        <itemBody>
          {question_html_xml}
          <response_str ident="response1" rcardinality="Single">
            <render_fib>
              <response_label ident="answer1" rshuffle="No"/>
            </render_fib>
          </response_str>
        </itemBody>
'''

ITEM_PRESENTATION_UPLOAD = '''\
        <itemBody>
          {question_html_xml}
        </itemBody>
'''

ITEM_PRESENTATION_NUM = '''\
        <itemBody>
          {question_html_xml}
          <response_str ident="response1" rcardinality="Single">
            <render_fib fibtype="Decimal">
              <response_label ident="answer1"/>
            </render_fib>
          </response_str>
        </itemBody>
'''

ITEM_RESPONSE_DECLARATION_MCTF = '''\
  <responseDeclaration identifier="RESPONSE" baseType="identifier" cardinality="single">
    <correctResponse>
      <value>text2qti_choice_{correct_choice}</value>
    </correctResponse>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float" normalMaximum="1" normalMinimum="0">
    <defaultValue>
      <value>0</value>
    </defaultValue>
  </outcomeDeclaration>
'''

ITEM_RESPONSE_DECLARATION_MULTANS = '''\
  <responseDeclaration identifier="RESPONSE" cardinality="multiple" baseType="identifier">
    <correctResponse>
      {correctResponses}
    </correctResponse>
    <mapping lowerBound="0" upperBound="{correctResponsesCount}" defaultValue="{defaultValue}">
      {mappings}
    </mapping>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float"/>  
'''


ITEM_RESPONSE_DECLARATION_CORRECT_RESPONSE = '''\
      <value>{ident}</value>
'''

ITEM_RESPONSE_DECLARATION_MAPPING_CORRECT = '''\
      <mapEntry mapKey="{ident}" mappedValue="1" />
'''

ITEM_RESPONSE_DECLARATION_MAPPING_INCORRECT = '''\
      <mapEntry mapKey="{ident}" mappedValue="-1" />
'''

ITEM_RESPONSE_DECLARATION_SHORTANS = '''\
  <responseDeclaration identifier="RESPONSE" cardinality="single" baseType="string">
    <correctResponse>
      {correctResponses}
    </correctResponse>
    <mapping defaultValue="0">
      {mapping}
    </mapping>
  </responseDeclaration>
  <outcomeDeclaration identifier="SCORE" cardinality="single" baseType="float" normalMaximum="1" normalMinimum="0">
    <defaultValue>
      <value>0.0</value>
    </defaultValue>
  </outcomeDeclaration>
'''

ITEM_RESPROCESSING_START = '''\
        <responseProcessing xmlns="http://www.imsglobal.org/xsd/imsqti_v2p1"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.imsglobal.org/xsd/imsqti_v2p1
            http://www.imsglobal.org/xsd/qti/qtiv2p1/imsqti_v2p1p2.xsd">
            <responseCondition>
                <responseIf>
                    <match>
                        <variable identifier="RESPONSE"/>
                        <correct identifier="RESPONSE"/>
                    </match>
                    <setOutcomeValue identifier="SCORE">
                        <baseValue baseType="float">1</baseValue>
                    </setOutcomeValue>
                </responseIf>
                <responseElse>
                    <setOutcomeValue identifier="SCORE">
                        <baseValue baseType="float">0</baseValue>
                    </setOutcomeValue>
                </responseElse>
            </responseCondition>
'''

ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <other/>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_MCTF_CHOICE_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <varequal respident="response1">{ident}</varequal>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="{ident}_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_MCTF_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <varequal respident="response1">{ident}</varequal>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_MCTF_SET_CORRECT_NO_FEEDBACK = '''\
'''

ITEM_RESPROCESSING_MCTF_INCORRECT_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <other/>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="general_incorrect_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_SHORTANS_GENERAL_FEEDBACK = ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK

ITEM_RESPROCESSING_SHORTANS_CHOICE_FEEDBACK = '''\
          <respcondition continue="Yes">
            <conditionvar>
              <varequal respident="response1">{answer_xml}</varequal>
            </conditionvar>
            <displayfeedback feedbacktype="Response" linkrefid="{ident}_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
{varequal}
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_NO_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
{varequal}
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
'''

ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_VAREQUAL = '''\
              <varequal respident="response1">{answer_xml}</varequal>'''

ITEM_RESPROCESSING_SHORTANS_INCORRECT_FEEDBACK = ITEM_RESPROCESSING_MCTF_INCORRECT_FEEDBACK

ITEM_RESPROCESSING_MULTANS_GENERAL_FEEDBACK = ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK

ITEM_RESPROCESSING_MULTANS_CHOICE_FEEDBACK = ITEM_RESPROCESSING_MCTF_CHOICE_FEEDBACK

ITEM_RESPROCESSING_MULTANS_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <and>
{varequal}
              </and>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_MULTANS_SET_CORRECT_NO_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <and>
{varequal}
              </and>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
'''

ITEM_RESPROCESSING_MULTANS_SET_CORRECT_VAREQUAL_CORRECT = '''\
                <varequal respident="response1">{ident}</varequal>'''

ITEM_RESPROCESSING_MULTANS_SET_CORRECT_VAREQUAL_INCORRECT = '''\
                <not>
                  <varequal respident="response1">{ident}</varequal>
                </not>'''

ITEM_RESPROCESSING_MULTANS_INCORRECT_FEEDBACK = ITEM_RESPROCESSING_MCTF_INCORRECT_FEEDBACK

ITEM_RESPROCESSING_ESSAY_GENERAL_FEEDBACK = ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK

ITEM_RESPROCESSING_UPLOAD_GENERAL_FEEDBACK = ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK

ITEM_RESPROCESSING_NUM_GENERAL_FEEDBACK = ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK

ITEM_RESPROCESSING_NUM_RANGE_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <vargte respident="response1">{num_min}</vargte>
              <varlte respident="response1">{num_max}</varlte>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_NUM_RANGE_SET_CORRECT_NO_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <vargte respident="response1">{num_min}</vargte>
              <varlte respident="response1">{num_max}</varlte>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
'''

ITEM_RESPROCESSING_NUM_EXACT_SET_CORRECT_WITH_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <or>
                <varequal respident="response1">{num_exact}</varequal>
                <and>
                  <vargte respident="response1">{num_min}</vargte>
                  <varlte respident="response1">{num_max}</varlte>
                </and>
              </or>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
            <displayfeedback feedbacktype="Response" linkrefid="correct_fb"/>
          </respcondition>
'''

ITEM_RESPROCESSING_NUM_EXACT_SET_CORRECT_NO_FEEDBACK = '''\
          <respcondition continue="No">
            <conditionvar>
              <or>
                <varequal respident="response1">{num_exact}</varequal>
                <and>
                  <vargte respident="response1">{num_min}</vargte>
                  <varlte respident="response1">{num_max}</varlte>
                </and>
              </or>
            </conditionvar>
            <setvar action="Set" varname="SCORE">100</setvar>
          </respcondition>
'''

ITEM_RESPROCESSING_NUM_INCORRECT_FEEDBACK = ITEM_RESPROCESSING_MCTF_INCORRECT_FEEDBACK

ITEM_RESPROCESSING_ESSAY = '''\
          <respcondition continue="No">
            <conditionvar>
              <other/>
            </conditionvar>
          </respcondition>
'''



ITEM_RESPROCESSING_END = '''\
        </responseProcessing>
'''


ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_GENERAL = '''\
        <itemfeedback ident="general_fb">
          <flow_mat>
            {feedback}
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_CORRECT = '''\
        <itemfeedback ident="correct_fb">
          <flow_mat>
            {feedback}
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_INCORRECT = '''\
        <itemfeedback ident="general_incorrect_fb">
          <flow_mat>
            {feedback}
          </flow_mat>
        </itemfeedback>
'''

ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_INDIVIDUAL = '''\
        <itemfeedback ident="{ident}_fb">
          <flow_mat>
            {feedback}
          </flow_mat>
        </itemfeedback>
'''




def assessment(*, quiz: Quiz, assessment_identifier: str, title_xml: str) -> str:
    '''
    Generate assessment XML from Quiz.
    '''
    xml = []
    xml.append(BEFORE_ITEMS.format(assessment_identifier=assessment_identifier,
                                   title=title_xml))
    for question_or_delim in quiz.questions_and_delims:
        if isinstance(question_or_delim, TextRegion):
            xml.append(TEXT.format(ident=f'text2qti_text_{question_or_delim.id}',
                                   text_title_xml=question_or_delim.title_xml,
                                   assessment_question_identifierref=f'text2qti_question_ref_{question_or_delim.id}',
                                   text_html_xml=question_or_delim.text_html_xml))
            continue
        if isinstance(question_or_delim, GroupStart):
            xml.append(GROUP_START.format(ident=f'text2qti_group_{question_or_delim.group.id}',
                                          group_title=question_or_delim.group.title_xml,
                                          pick=question_or_delim.group.pick,
                                          points_per_item=question_or_delim.group.points_per_question))
            continue
        if isinstance(question_or_delim, GroupEnd):
            xml.append(GROUP_END)
            continue
        if not isinstance(question_or_delim, Question):
            raise TypeError
        question = question_or_delim

        xml.append(START_ITEM.format(question_identifier=f'text2qti_question_{question.id}',
                                     question_title=question.title_xml))

        if question.type in ('true_false_question', 'multiple_choice_question',
                             'short_answer_question', 'multiple_answers_question'):
            item_metadata = ITEM_METADATA_MCTF_SHORTANS_MULTANS_NUM
            original_answer_ids = ','.join(f'text2qti_choice_{c.id}' for c in question.choices)
        elif question.type == 'numerical_question':
            item_metadata = ITEM_METADATA_MCTF_SHORTANS_MULTANS_NUM
            original_answer_ids = f'text2qti_numerical_{question.id}'
        elif question.type == 'essay_question':
            item_metadata = ITEM_METADATA_ESSAY
            original_answer_ids = f'text2qti_essay_{question.id}'
        elif question.type == 'file_upload_question':
            item_metadata = ITEM_METADATA_UPLOAD
            original_answer_ids = f'text2qti_upload_{question.id}'
        else:
            raise ValueError
        xml.append(item_metadata.format(question_type=question.type,
                                        points_possible=question.points_possible,
                                        original_answer_ids=original_answer_ids,
                                        assessment_question_identifierref=f'text2qti_question_ref_{question.id}'))

        if question.type in ('true_false_question', 'multiple_choice_question'):
            correct_choice = None
            for choice in question.choices:
                if choice.correct:
                  correct_choice = choice
                  break
            if correct_choice is None:
                raise TypeError
            
            xml.append(ITEM_RESPONSE_DECLARATION_MCTF.format(correct_choice=correct_choice.id))
        elif question.type in ('multiple_answers_question'):
          correctResponses = []
          mappings = []
          for choice in question.choices:
                if choice.correct:
                  correctResponses.append(ITEM_RESPONSE_DECLARATION_CORRECT_RESPONSE.format(ident=f'text2qti_choice_{choice.id}'))
                  mappings.append(ITEM_RESPONSE_DECLARATION_MAPPING_CORRECT.format(ident=f'text2qti_choice_{choice.id}'))
                else:
                  mappings.append(ITEM_RESPONSE_DECLARATION_MAPPING_INCORRECT.format(ident=f'text2qti_choice_{choice.id}'))
          
          xml.append(ITEM_RESPONSE_DECLARATION_MULTANS.format(
            correctResponses="".join(correctResponses),
            correctResponsesCount=len(correctResponses),
            mappings="".join(mappings),
            defaultValue=-len(correctResponses)+1
          ))
        elif question.type == 'short_answer_question':
          mapping=[]
          correctResponses=[]
          for choice in question.choices:
              correctResponses.append(ITEM_RESPONSE_DECLARATION_CORRECT_RESPONSE.format(ident=choice.choice_xml))
              mapping.append(ITEM_RESPONSE_DECLARATION_MAPPING_CORRECT.format(ident=choice.choice_xml))
          xml.append(ITEM_RESPONSE_DECLARATION_SHORTANS.format(
            correctResponses="".join(correctResponses),
            mapping="".join(mapping)))


        if question.type in ('true_false_question', 'multiple_choice_question', 'multiple_answers_question'):
            if question.type in ('true_false_question', 'multiple_choice_question'):
                item_presentation_choice = ITEM_PRESENTATION_MCTF_CHOICE
                item_presentation = ITEM_PRESENTATION_MCTF
            elif question.type == 'multiple_answers_question':
                item_presentation_choice = ITEM_PRESENTATION_MULTANS_CHOICE
                item_presentation = ITEM_PRESENTATION_MULTANS
            else:
                raise ValueError
            choices = '\n'.join(item_presentation_choice.format(ident=f'text2qti_choice_{c.id}', choice_html_xml=c.choice_html_xml)
                                                                for c in question.choices)
            xml.append(item_presentation.format(question_html_xml=question.question_html_xml, choices=choices, maxChoices=len(question.choices)))
        elif question.type == 'short_answer_question':
            xml.append(ITEM_PRESENTATION_SHORTANS.format(question_html_xml=question.question_html_xml))
        elif question.type == 'numerical_question':
            xml.append(ITEM_PRESENTATION_NUM.format(question_html_xml=question.question_html_xml))
        elif question.type == 'essay_question':
            xml.append(ITEM_PRESENTATION_ESSAY.format(question_html_xml=question.question_html_xml))
        elif question.type == 'file_upload_question':
            xml.append(ITEM_PRESENTATION_UPLOAD.format(question_html_xml=question.question_html_xml))
        else:
            raise ValueError

        if question.type in ('true_false_question', 'multiple_choice_question'):
            correct_choice = None
            for choice in question.choices:
                if choice.correct:
                  correct_choice = choice
                  break
            if correct_choice is None:
                raise TypeError
            resprocessing = []
            resprocessing.append(ITEM_RESPROCESSING_START)
            if question.feedback_raw is not None:
                resprocessing.append(ITEM_RESPROCESSING_MCTF_GENERAL_FEEDBACK)
            for choice in question.choices:
                if choice.feedback_raw is not None:
                    resprocessing.append(ITEM_RESPROCESSING_MCTF_CHOICE_FEEDBACK.format(ident=f'text2qti_choice_{choice.id}'))
            if question.correct_feedback_raw is not None:
                resprocessing.append(ITEM_RESPROCESSING_MCTF_SET_CORRECT_WITH_FEEDBACK.format(ident=f'text2qti_choice_{correct_choice.id}'))
            else:
                resprocessing.append(ITEM_RESPROCESSING_MCTF_SET_CORRECT_NO_FEEDBACK.format(ident=f'text2qti_choice_{correct_choice.id}'))
            if question.incorrect_feedback_raw is not None:
                resprocessing.append(ITEM_RESPROCESSING_MCTF_INCORRECT_FEEDBACK)
            resprocessing.append(ITEM_RESPROCESSING_END)
            xml.extend(resprocessing)
        elif question.type == 'short_answer_question':
            resprocessing = []
            resprocessing.append(ITEM_RESPROCESSING_START)
            # if question.feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_SHORTANS_GENERAL_FEEDBACK)
            # for choice in question.choices:
            #     if choice.feedback_raw is not None:
            #         resprocessing.append(ITEM_RESPROCESSING_SHORTANS_CHOICE_FEEDBACK.format(ident=f'text2qti_choice_{choice.id}', answer_xml=choice.choice_xml))
            # varequal = []
            # for choice in question.choices:
            #     varequal.append(ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_VAREQUAL.format(answer_xml=choice.choice_xml))
            # if question.correct_feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_WITH_FEEDBACK.format(varequal='\n'.join(varequal)))
            # else:
            #     resprocessing.append(ITEM_RESPROCESSING_SHORTANS_SET_CORRECT_NO_FEEDBACK.format(varequal='\n'.join(varequal)))
            # if question.incorrect_feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_SHORTANS_INCORRECT_FEEDBACK)
            resprocessing.append(ITEM_RESPROCESSING_END)
            xml.extend(resprocessing)
        elif question.type == 'multiple_answers_question':
            resprocessing = []
            resprocessing.append(ITEM_RESPROCESSING_START)
            # if question.feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_MULTANS_GENERAL_FEEDBACK)
            # for choice in question.choices:
            #     if choice.feedback_raw is not None:
            #         resprocessing.append(ITEM_RESPROCESSING_MULTANS_CHOICE_FEEDBACK.format(ident=f'text2qti_choice_{choice.id}'))
            # varequal = []
            # for choice in question.choices:
            #     if choice.correct:
            #         varequal.append(ITEM_RESPROCESSING_MULTANS_SET_CORRECT_VAREQUAL_CORRECT.format(ident=f'text2qti_choice_{choice.id}'))
            #     else:
            #         varequal.append(ITEM_RESPROCESSING_MULTANS_SET_CORRECT_VAREQUAL_INCORRECT.format(ident=f'text2qti_choice_{choice.id}'))
            # if question.correct_feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_MULTANS_SET_CORRECT_WITH_FEEDBACK.format(varequal='\n'.join(varequal)))
            # else:
            #     resprocessing.append(ITEM_RESPROCESSING_MULTANS_SET_CORRECT_NO_FEEDBACK.format(varequal='\n'.join(varequal)))
            # if question.incorrect_feedback_raw is not None:
            #     resprocessing.append(ITEM_RESPROCESSING_MULTANS_INCORRECT_FEEDBACK)
            resprocessing.append(ITEM_RESPROCESSING_END)
            xml.extend(resprocessing)
        elif question.type == 'numerical_question':
            xml.append(ITEM_RESPROCESSING_START)
            if question.feedback_raw is not None:
              xml.append(ITEM_RESPROCESSING_NUM_GENERAL_FEEDBACK)
            if question.correct_feedback_raw is None:
                if question.numerical_exact is None:
                    item_resprocessing_num_set_correct = ITEM_RESPROCESSING_NUM_RANGE_SET_CORRECT_NO_FEEDBACK
                else:
                    item_resprocessing_num_set_correct = ITEM_RESPROCESSING_NUM_EXACT_SET_CORRECT_NO_FEEDBACK
            else:
                if question.numerical_exact is None:
                    item_resprocessing_num_set_correct = ITEM_RESPROCESSING_NUM_RANGE_SET_CORRECT_WITH_FEEDBACK
                else:
                    item_resprocessing_num_set_correct = ITEM_RESPROCESSING_NUM_EXACT_SET_CORRECT_WITH_FEEDBACK
            xml.append(item_resprocessing_num_set_correct.format(num_min=question.numerical_min_html_xml,
                                                                 num_exact=question.numerical_exact_html_xml,
                                                                 num_max=question.numerical_max_html_xml))
            if question.incorrect_feedback_raw is not None:
                xml.append(ITEM_RESPROCESSING_NUM_INCORRECT_FEEDBACK)
            xml.append(ITEM_RESPROCESSING_END)
        elif question.type == 'essay_question':
            xml.append(ITEM_RESPROCESSING_START)
            xml.append(ITEM_RESPROCESSING_ESSAY)
            if question.feedback_raw is not None:
                xml.append(ITEM_RESPROCESSING_ESSAY_GENERAL_FEEDBACK)
            xml.append(ITEM_RESPROCESSING_END)
        elif question.type == 'file_upload_question':
            xml.append(ITEM_RESPROCESSING_START)
            if question.feedback_raw is not None:
                xml.append(ITEM_RESPROCESSING_UPLOAD_GENERAL_FEEDBACK)
            xml.append(ITEM_RESPROCESSING_END)
        else:
            raise ValueError

        if question.type in ('true_false_question', 'multiple_choice_question',
                             'short_answer_question', 'multiple_answers_question',
                             'numerical_question', 'essay_question', 'file_upload_question'):
            if question.feedback_raw is not None:
                xml.append(ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_GENERAL.format(feedback=question.feedback_html_xml))
            if question.correct_feedback_raw is not None:
                xml.append(ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_CORRECT.format(feedback=question.correct_feedback_html_xml))
            if question.incorrect_feedback_raw is not None:
                xml.append(ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_INCORRECT.format(feedback=question.incorrect_feedback_html_xml))
        if question.type in ('true_false_question', 'multiple_choice_question',
                             'short_answer_question', 'multiple_answers_question'):
            for choice in question.choices:
                if choice.feedback_raw is not None:
                    xml.append(ITEM_FEEDBACK_MCTF_SHORTANS_MULTANS_NUM_INDIVIDUAL.format(ident=f'text2qti_choice_{choice.id}',
                                                                                         feedback=choice.feedback_html_xml))

        xml.append(END_ITEM)

    xml.append(AFTER_ITEMS.format(assessment_identifier=assessment_identifier))

    return ''.join(xml)
