library(shiny)
library(gdata)
library(RWeka)
# Define server logic required to draw a histogram
shinyServer(function(input, output) {
    
    # Expression that generates a histogram. The expression is
    # wrapped in a call to renderPlot to indicate that:
    #
    #  1) It is "reactive" and therefore should re-execute automatically
    #     when inputs change
    #  2) Its output type is a plot
    resulttext <- eventReactive(input$goButton, {
        trigram_prediction(input$sentence)
        
    })
    
    output$output1 <- renderText(
        resulttext()[1]
    )
    
     output$output2 <- renderText(
          resulttext()[2]
      )
     
     output$output3 <- renderText(
         resulttext()[3]
     )
     
     output$selection <- eventReactive(input$goButton2, {
         
         resulttext()[as.integer(input$choice)]
         
     })
     output$result <- eventReactive(input$goButton2, {
         
         paste(input$sentence, resulttext()[as.integer(input$choice)])
         
     })
})