library(shiny)
library(ggplot2)
load("AppEnvironment.RData")
shinyUI(
    navbarPage("Demystifying the Ivory Tower",
               tabPanel("General Descriptive Analysis",
                    sidebarLayout(
                        sidebarPanel(
                            p("Histogram of attribute will be displayed."),
                            p("In case of adjusting factors, multiple graphs will be displayed"),
                            selectInput("Attrib", "Attributes", c("Earning After Graduation" = "md_earn_wne_p8", "Graduation rate" = "C150_4", "Median Debt" = "GRAD_DEBT_MDN", "Admission Rate" = "ADM_RATE", "Student Population" = "UGDS", "SAT Math Score" = "SATMTMID", "SAT Verbal Score" = "SATVRMID", "Average Fmaily Income" = "AVG_INC", "Cost of Education" = "COSTT4_A", "ROI" = "ROI", "Full Time Faculty Percentage" = "PFTFAC")),
                            selectInput("Factor", "Adjusting Factors", c("Region" = "region", "Locale" = "LOCALE", "Type of School" = "Major_Cluster", "Cost Level" = "cost_level", "None" = "NULL"), selected = "None"),
                            submitButton("Apply Selection")
                             ),
                        
                        mainPanel(
                            p("Here is where the graph lies"),
                            plotOutput("plot1"),
                            verbatimTextOutput("table1")
                            
                        )
                    )
                        
                        
                        ),
               
               tabPanel("Look-Up Tools (College Listing)",
                    fluidPage(
                        fluidRow(
                            column(3,selectInput("type", "College Type", c("All", "Specialized", "Comprehensive", "Professional"), selected = "All")),
                            column(3,selectInput("reg", "Region", c("All","New England", "Mid East", "Great Lakes", "Plains", "Southeast", "Southwest", "Rocky Mountains", "Far West", "Others"), selected = "All")),
                            column(3,selectInput("pop", "Undergraduate Population", c("All", "High (>30,000)" = "High", "Medium (10,000-30,000)" = "Medium", "Low (<10,000)" = "Low"))),
                            column(3,selectInput("locale", "Locale", c("All", "City:Large", "City:Midsize", "City:Small", "Suburb:Large", "Suburb:Midsize", "Suburb:Small", "Town:Fringe", "Town:Distant", "Town:Remote", "Rural:Fringe", "Rural:Distant", "Rural:Remote"), selected = "All"))),
                        
                        fluidRow(    
                            column(3,selectInput("cost", "Cost Level", c("All","High (>$40,000)" = "High", "Medium ($20,000-$40,000)" = "Medium", "Low (<$20,000)" = "Low"), selected = "All")),
                            column(3,selectInput("re", "Future Income", c( "All","High (>$50,000)" = "High", "Medium ($25,000-$50,000)" = "Medium", "Low (<$25,000)" = "Low"), selected = "All")),
                            column(3,selectInput("debt", "Debt After Graduation", c("All","High (>$30,000)" = "High", "Medium ($15,000-$30,000)" = "Medium","Low (<$15,000)" = "Low") , selected = "All")),
                            column(3,selectInput("admin", "Admission Rate", c("All", "High (>66%)" = "High", "Medium (33%-66%)" = "Medium", "Low (<33%)" = "Low"), selected = "All"))),
                        
                        fluidRow(
                            column(3,selectInput("grad", "Graduation Rate", c("All", "High (>66%)" = "High", "Medium (33%-66%)" = "Medium", "Low (<33%)" = "Low"), selected = "All")),
                            column(3,selectInput("math", "SAT Math", c("All", "High (>650)" = "High", "Medium (450-650)" = "Medium", "Low (<450)" = "Low"), selected = "All")),
                            column(3,selectInput("verbal", "SAT Verbal", c("All", "High (>650)" = "High", "Medium (450-650)" = "Medium", "Low (<450)" = "Low"), selected = "All")),
                            column(3,selectInput("fam", "Family Income", c("All", "High (>$70,000)" = "High", "Medium ($30,000-$70,000)" = "Medium", "Low (<$30,000)" = "Low"), selected = "All"))),
                        
                        fluidRow(    
                        submitButton("Display Results")
                        ),
                        
                        fluidRow(
                            dataTableOutput("dt")
                        )
                        
                            )
                        
                        ),
               tabPanel("College Look-Up", 
                    fluidPage(
                        fluidRow(
                            textInput("name", "Institution Name")
                           
                        ),
                        
                        fluidRow(
                            submitButton("Apply Selection")
                        ),
                        
                        fluidRow(
                            dataTableOutput("dt2")
                        )
                    )
                        
               ),
                        
                        
               tabPanel("Prediction Tools",
                    sidebarLayout(
                        sidebarPanel(
                            p("This is a sidebar that showcases our prediction model"),
                            p("Please enter desired information to predict the ROI of any college"),
                            numericInput("p_pop", "Undergraduate Population", 20000),
                            numericInput("p_debt", "Debt After Graduation", 20000),
                            selectInput("p_type", "College Type", c("Specialized", "Comprehensive", "Professional")),
                            selectInput("p_reg", "Region", c("New England", "Mid East", "Great Lakes", "Plains", "Southeast", "Southwest", "Rocky Mountains", "Far West", "Others")),
                            selectInput("p_cost", "Cost Level", c("High", "Low")),
                            selectInput("p_locale", "Locale", c("City:Large", "City:Midsize", "City:Small", "Suburb:Large", "Suburb:Midsize", "Suburb:Small", "Town:Fringe", "Town:Distant", "Town:Remote", "Rural:Fringe", "Rural:Distant", "Rural:Remote")),
                            numericInput("p_grad", "Graduation Rate", .5),
                            numericInput("p_adm", "Admission Rate", 0.5),
                            numericInput("p_avg_inc", "Average Family Income", 20000),
                            numericInput("p_satvar", "SAT Verbal", 500),
                            numericInput("p_satmt", "SAT Math", 500),
                            numericInput("p_full", "Percentage Fulltime Faculty", 0.5),
                            selectInput("test", "Select Test Type", c("Classification" = "c", "Regression" = "r")),
                            submitButton("Display Results")
                            
                        ),
                        
                        mainPanel(
                            p("Prediction Output:"),
                            br(),
                            verbatimTextOutput("prediction"),
                            br(),
                            p("Attribute Importance Rating"),
                            br(),
                            verbatimTextOutput("importance"),
                            br(),
                            p("Model's Error: confusion matrix for Classification and R squared for Regression"),
                            br(),
                            verbatimTextOutput("error"),
                            br()
                        )
                    )
                        
                        
                        )
  )
)