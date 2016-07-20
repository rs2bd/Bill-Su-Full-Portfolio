library(shiny)
library(gdata)
library(RWeka)

attach("AppEnv.RData")

shinyUI(fluidPage(
    
    # Application title
    titlePanel("Language Prediction"),
    
    # Sidebar with instructions
    sidebarLayout(
        sidebarPanel(
            textInput("sentence",
                      "Please enter the sentence:"
                      
            ),
            actionButton("goButton", "Go!"),
            h4("The Options Are: "),
            strong("Machine Preferred Answer:   "), textOutput("output1"),
            strong("Alt 1:   "), textOutput("output2"),
            strong("Alt 2:   "), textOutput("output3"),
            
            
            radioButtons("choice", h4("Please Select Options: "),
                         c("Machine Preferred Answer" = 1,
                           "Alt 2" = 2,
                           "Alt 3" = 3
                         )),
            
            actionButton("goButton2", "Go!"),
            h4("You have selected: "),
            textOutput("selection"),
            h4("Below Display Your Final Sentence:"),
            textOutput("result")
        ),
        
        mainPanel(
            h2("Feature Introduction"),
            
            tags$li("This is a simple shiny application designed to predict the next word given a sentence."),
            tags$li("Instead of solely relying on our model to give you the prediction, we partially rely on your judgement 
              to give us the most accurate answer"),
            tags$li("You will see five options after you type in your sentence and click GO!"),
            tags$li("You will be able to select the best answer you want from those five and we will produce a complete sentence afterward"),
            tags$li("<e> stands for ending of a sentence"),
            tags$li("Please ONLY enter sentence size 2 or more"),
            h4("Enjoy the application!")
            
            
        )
    )
))
