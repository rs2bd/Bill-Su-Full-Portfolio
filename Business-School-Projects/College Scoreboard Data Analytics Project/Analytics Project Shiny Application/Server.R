library(shiny)
library(RWeka)
library(dplyr)
library(googleVis)
library(scales)
library(psych)
library(randomForest)
load("AppEnvironment.RData")
shinyServer(function(input, output) {
    
    selectedData <- reactive({
        dataset[,input$Attrib]
    })
    
    factors <- reactive({
        dataset[,input$Factor]
    })
#   
#     output$plot1 <- renderPlot({
#         if (!is.null(factors())){
#         plot1 <- ggplot(data = dataset, aes(x = "ROI", color = "cost_level"))}
#         else {plot1 <- ggplot(selectedData())}
#         hist(dataset[,selectedData])
#     }
    output$plot1 <- renderPlot({
        if (input$Attrib != "NULL"){
        ggplot(dataset, aes_string(x = input$Attrib, color = input$Factor)) + geom_density() + xlab(input$Attrib) + ylab("Count") + scale_y_continuous(labels = comma) + scale_x_continuous(labels = comma)}
        else{ ggplot(dataset, aes_string(x=input$Attrib) + geom_density() + xlab(input$Attrib) + ylab("Count")) + scale_y_continuous(labels = comma) + scale_x_continuous(labels =comma)}
    })
    
    output$table1 <- renderPrint({
        if (input$Factor != "NULL"){
            describeBy(subset(dataset, select = c(input$Attrib, input$Factor)), group = input$Factor,na.rm = TRUE)}
        else {
            describe(selectedData())}
        
    })
    
    output$dt <- renderDataTable({
        dt <- dataset
        
        if (input$re == "High"){
            dt = filter(dt, md_earn_wne_p8 > 50000 )}
        else if (input$re == "Medium"){
            dt = filter(dt, md_earn_wne_p8 > 25000, md_earn_wne_p8 < 50000 )}
        else if (input$re == "Low"){
            dt = filter(dt, md_earn_wne_p8 < 25000)}
        
        if (input$admin == "High"){
            dt = filter(dt, ADM_RATE > 0.66 )}
        else if (input$admin == "Medium"){
            dt = filter(dt, ADM_RATE < 0.66, ADM_RATE > 0.33)}
        else if (input$admin == "Low"){
            dt = filter(dt, ADM_RATE < 0.33)}
        
        if (input$grad == "High"){
            dt = filter(dt, C150_4 > 0.66 )}
        else if (input$grad == "Medium"){
            dt = filter(dt, C150_4 < 0.66, C150_4 > 0.33)}
        else if (input$grad == "Low"){
            dt = filter(dt, C150_4 < 0.33)}
        
        if (input$debt == "High"){
            dt = filter(dt, GRAD_DEBT_MDN > 30000)}
        else if (input$debt == "Medium"){
            dt = filter(dt, GRAD_DEBT_MDN < 30000, GRAD_DEBT_MDN > 15000)}
        else if (input$debt == "Low"){
            dt = filter(dt, GRAD_DEBT_MDN < 15000)}
        
        
        if (input$pop == "High"){
            dt = filter(dt, UGDS > 30000)}
        else if (input$pop == "Medium"){
            dt = filter(dt, UGDS < 30000, UGDS > 10000)}
        else if (input$pop == "Low"){
            dt = filter(dt, UGDS < 10000)}
        
        
        if (input$math == "High"){
            dt = filter(dt, SATMTMID > 650)}
        else if (input$math == "Medium"){
            dt = filter(dt, SATMTMID < 650, SATMTMID > 450)}
        else if (input$math == "Low"){
            dt = filter(dt, SATMTMID < 450)}
        
        if (input$verbal == "High"){
            dt = filter(dt, SATVRMID > 650)}
        else if (input$verbal == "Medium"){
            dt = filter(dt, SATVRMID < 650, SATVRMID > 450)}
        else if (input$verbal == "Low"){
            dt = filter(dt, SATVRMID < 450)}
        
        if (input$fam == "High"){
            dt = filter(dt, AVG_INC > 70000)}
        else if (input$fam == "Medium"){
            dt = filter(dt, AVG_INC < 70000, AVG_INC > 30000)}
        else if (input$fam == "Low"){
            dt = filter(dt, AVG_INC < 30000)}
        
        if (input$cost == "High"){
            dt = filter(dt, COSTT4_A > 40000)}
        else if (input$cost == "Medium"){
            dt = filter(dt, COSTT4_A > 20000, COSTT4_A < 40000)}
        else if (input$cost == "Low"){
            dt = filter(dt, COSTT4_A < 20000)}
        
        if (input$locale != "All"){
            dt = filter(dt, LOCALE == input$locale)
        }
        
        if (input$type != "All"){
            dt = filter(dt, Major_Cluster == input$type)
        }
        
        if (input$reg != "All"){
            dt = filter(dt, region == input$reg)
        }
        
        
        dt = rename(dt, id = UNITID, name = INSTNM, city = CITY, region = region, state = STABBR, locale = LOCALE, type = Major_Cluster, 
                    cost = COSTT4_A, eight_year_income = md_earn_wne_p8, ROI = ROI, family_income = AVG_INC, debt_after_graduation = GRAD_DEBT_MDN, admission_rate = ADM_RATE,
                    graduation_rate = C150_4, SAT_math = SATMTMID, SAT_verbal = SATVRMID, percentage_full_time_faculty = PFTFAC, undergraduate_population = UGDS)
        
        dt = dt[,c("id", "name", "undergraduate_population", "city", "region", "state", "locale", "type", "cost", "eight_year_income", "ROI", "family_income", "debt_after_graduation", "admission_rate",
                   "graduation_rate", "SAT_math", "SAT_verbal", "percentage_full_time_faculty")]
        dt
    })
    
    output$dt2 <- renderDataTable({
        dt = filter(dataset, INSTNM == input$name)
        dt = rename(dt, id = UNITID, name = INSTNM, city = CITY, region = region, state = STABBR, locale = LOCALE, type = Major_Cluster, 
                    cost = COSTT4_A, eight_year_income = md_earn_wne_p8, ROI = ROI, family_income = AVG_INC, debt_after_graduation = GRAD_DEBT_MDN, admission_rate = ADM_RATE,
                    graduation_rate = C150_4, SAT_math = SATMTMID, SAT_verbal = SATVRMID, percentage_full_time_faculty = PFTFAC, undergraduate_population = UGDS)
        
        dt = dt[,c("id", "name", "undergraduate_population", "city", "region", "state", "locale", "type", "cost", "eight_year_income", "ROI", "family_income", "debt_after_graduation", "admission_rate",
                   "graduation_rate", "SAT_math", "SAT_verbal", "percentage_full_time_faculty")]
        dt
    })
    
    output$prediction <- renderPrint({
        
        test <- data.frame("region" = input$p_reg, "LOCALE" = input$p_locale, "Major_Cluster" =input$p_type,
                           "AVG_INC" = input$p_avg_inc, "GRAD_DEBT_MDN" = input$p_debt, "ADM_RATE" = input$p_adm,
                           "C150_4" = input$p_grad, "SATMTMID" = input$p_satmt, "SATVRMID" = input$p_satvar, 
                           "PFTFAC" = input$p_full, "UGDS" = input$p_pop, "cost_level" = input$p_cost)
        levels(test$LOCALE) = levels(rf_output$LOCALE)
        levels(test$region) = levels(rf_output$region)
        levels(test$Major_Cluster) = levels(rf_output$Major_Cluster)
        levels(test$cost_level) = levels(rf_output$cost_level)
        test[1, "LOCALE"] <- input$p_locale 
        test[1, "region"] <- input$p_reg 
        test[1, "Major_Cluster"] <- input$p_type 
        test[1, "cost_level"] <-input$p_cost
        if (input$test == "c") {
            randomForest:::predict.randomForest(model, newdata = test)
        }
        else if (input$test == "r"){
            randomForest:::predict.randomForest(model_reg, newdata = test)
        }
    })
    
    output$error <- renderPrint({
        if (input$test == "c") {
            model$confusion
        }
        else if (input$test == "r"){
            model_reg$rsq
        }
    })
    
    output$importance <- renderPrint({
        if (input$test == "c") {
            model$importance
        }
        else if (input$test == "r"){
            model_reg$importance
        }
    })
}
)
