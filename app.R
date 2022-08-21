library(shiny)
library(rvest)
library(dplyr)
library(reactable)
library(DT)
library(ggplot2)
library(tidyr)
library(shinyWidgets)

footballDB <- read.csv(file = 'Fantasy_Sheet.csv')

footballTable <- footballDB %>%
  rowwise() %>%
  mutate(
    avgRank = (mean(
      c(
        FantasyFootballCalc,
        BetIQ,
        FantasyPros,
        CBSRanking,
        ESPNRanking,
        FFPCRanking,
        BB10sRanking,
        NFLRanking,
        UnderdogRanking,
        YahooRanking
      ),
      na.rm = TRUE
    )),
    maxRank = (max(
      c(
        FantasyFootballCalc,
        BetIQ,
        FantasyPros,
        CBSRanking,
        ESPNRanking,
        FFPCRanking,
        BB10sRanking,
        NFLRanking,
        UnderdogRanking,
        YahooRanking
      ),
      na.rm = TRUE
    )),
    minRank = (min(
      c(
        FantasyFootballCalc,
        BetIQ,
        FantasyPros,
        CBSRanking,
        ESPNRanking,
        FFPCRanking,
        BB10sRanking,
        NFLRanking,
        UnderdogRanking,
        YahooRanking
      ),
      na.rm = TRUE
    )),
    medianRank = (median(
      c(
        FantasyFootballCalc,
        BetIQ,
        FantasyPros,
        CBSRanking,
        ESPNRanking,
        FFPCRanking,
        BB10sRanking,
        NFLRanking,
        UnderdogRanking,
        YahooRanking
      ),
      na.rm = TRUE
    )),
  ) %>%
  summarize(Name,
            Team,
            Position,
            avgRank,
            minRank,
            maxRank,
            medianRank)

footballTable <-
  tibble::rownames_to_column(footballTable, "Overall")
footballTable <- tibble::as_tibble(footballTable)

ui <- fluidPage(mainPanel(
  setBackgroundColor("black"),
  
  reactableOutput("table"),
  verbatimTextOutput("selection"),
  plotOutput("plotQB"),
  plotOutput("plotRB"),
  plotOutput("plotWR"),
  plotOutput("plotTE"),
  plotOutput("plotDST"),
  plotOutput("plotK")
))

server <- function(input, output) {
  
  output$table <- renderReactable({
    reactable(
      footballTable,
      selection = "multiple",
      showPageInfo = FALSE,
      showPageSizeOptions = TRUE,
      defaultPageSize = 25,
      borderless = TRUE,
      onClick = "select",
      filterable = TRUE,
      theme = reactableTheme(
        rowSelectedStyle = list(backgroundColor = "#000000", boxShadow = "inset 2px 0 0 0 #ffa62d")
      )
    )
  })
  
  output$selection <- renderPrint({
    reactable::getReactableState("table", name = "selected")
    
  })
  
  output$plotQB <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "QB") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("QB Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
  output$plotRB <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "RB") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("RB Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
  output$plotWR <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "WR") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("WR Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
  output$plotTE <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "TE") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("TE Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
  output$plotDST <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "DST") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("DST Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
  output$plotK <- renderPlot({
    data_plot <- footballDB %>%
      gather(key = "site", value = "pick", FantasyFootballCalc:YahooRanking) %>%
      drop_na() %>%
      group_by(Name) %>%
      summarise(avPick = mean(pick),
                pos = Position[1]) %>%
      mutate(round = ((avPick-1)%/%12)+1) %>%
      group_by(pos, round) %>%
      summarise(n = n())
    
    data_plot %>%
      filter(pos == "K") %>%
      ggplot(aes(x = round, y = n)) +
      geom_col() +
      ggtitle("K Draft Position") +
      theme_grey(base_size = 17) +
      scale_x_continuous(breaks = round(seq(min(1), max(32), by = 1),1)) +
      scale_y_continuous(breaks = round(seq(min(data_plot$n), max(data_plot$n), by = 1),1))
  })
  
}

# Run the application
shinyApp(ui = ui, server = server)
