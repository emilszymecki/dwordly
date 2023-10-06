*** Settings ***
Documentation       Playwright template.
Library             dwordly.py
Library             lib.py
Library             RPA.Browser.Playwright
Library             Collections


*** Tasks ***
Dwordly Solver
    Starting a browser
    Play Dwordly
    

*** Keywords ***

Starting a browser
    New Browser    chromium    headless=false    args=["--start-maximized"]
    New Context    viewport=${None}
    Set Browser Timeout    timeout=10s

Open Dwordly
    New Page       https://dwordly.fun/
    TRY
        Wait For Elements State    \#close-help-btn   timeout=2s
        Click    id=close-help-btn
    EXCEPT
        Log    Has not first modal
    END 
    Click    id=close-keyboard-banner-btn
    Wait For Elements State    \#played-words-list
    Sleep    1s
    ${first_word}=    Evaluate JavaScript    \#played-words-list > li
    ...    (elements, arg) => {
    ...        let text = elements.innerText.split("\\n").join('');
    ...        return text
    ...    }
    ...    all_elements=False
    ${path}=    find_path_to_one_letter_word    ${first_word}
    RETURN    ${path}



Dwordly Game
    [Arguments]   ${path}
    Log    ${path}
    ${first_word}=    Set Variable    ${path}[0]
    ${second_word}=    Set Variable    ${path}[1]
    ${diff}=    diff_words    ${first_word}    ${second_word}
    Dwordly Action    ${diff}
    Remove From List    ${path}    0
    ${finish}=    Get Element Count    \#message-banner[class="hidden"]
    IF    len(${path}) > 2 and ${finish} != 0
        Dwordly Game    ${path}
    ELSE
        Log    ${path}
        Log To Console    UDAŁO SIĘ!!!
        Close Page
        Play Dwordly
    END

Dwordly Action
    [Arguments]   ${action}
    ${action_type}=    Set Variable    ${action}[0]
    ${index}=    Set Variable    ${action}[1]
    ${letter}=    Set Variable    ${action}[2]
    Click    \#next-play > form > div.word > div:nth-child(${index+1})
    IF    '${action_type}' == 'remove'
        Click   \#next-play > form > div.word > div:nth-child(${index+1}) > button.remove-letter-btn
    ELSE
        Click    \#keyboard > form > button[value=${letter}]
    END
    Sleep    1s
    Click    \#play-word-btn
    Sleep    1s
    
Play Dwordly
    ${path}=    Open Dwordly
    Dwordly Game    ${path}


