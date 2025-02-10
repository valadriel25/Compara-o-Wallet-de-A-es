import yfinance as yf
import matplotlib.pyplot as plt
import datetime
import numpy as np

def fetch_stock_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(start=start_date, end=end_date)['Close']
    return data

def calculate_return_and_risk(data):
    returns = {}
    for ticker, prices in data.items():
        daily_returns = prices.pct_change().dropna()
        expected_return = daily_returns.mean()
        risk = daily_returns.std()
        returns[ticker] = (expected_return, risk, daily_returns)
    return returns

def plot_risk_return(returns):
    plt.figure(figsize=(10, 6))
    tickers = list(returns.keys())
    expected_returns = [returns[ticker][0] for ticker in tickers]
    risks = [returns[ticker][1] for ticker in tickers]

    plt.scatter(risks, expected_returns, color='blue')
    for i, ticker in enumerate(tickers):
        plt.annotate(ticker, (risks[i], expected_returns[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title('Risco vs Retorno Esperado')
    plt.xlabel('Risco (Desvio Padrão dos Retornos Diários)')
    plt.ylabel('Retorno Esperado (Média dos Retornos Diários)')
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_weight_allocation(tickers, weights):
    plt.figure(figsize=(8, 5))
    bars = plt.bar(tickers, weights, color='orange')
    plt.title('Alocação de Pesos da Carteira')
    plt.xlabel('Ativos')
    plt.ylabel('Peso (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y')

    # Adiciona os valores numéricos em cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}%', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def plot_return_risk_over_time(data):
    plt.figure(figsize=(12, 6))

    for ticker, prices in data.items():
        daily_returns = prices.pct_change().dropna()
        cumulative_returns = (1 + daily_returns).cumprod() - 1
        risk = daily_returns.rolling(window=5).std()  # Risco em uma janela de 5 dias

        plt.plot(cumulative_returns.index, cumulative_returns, label=f'Retorno Cumulativo {ticker}')
        plt.plot(risk.index, risk, linestyle='--', label=f'Risco {ticker}')

    plt.title('Evolução dos Retornos e Risco ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def main():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)  # Últimos 30 dias

    tickers = ["GOOGL", "AAPL", "MSFT"]

    print("Buscando dados das ações:", tickers)
    data = fetch_stock_data(tickers, start_date, end_date)

    if data:
        returns = calculate_return_and_risk(data)
        plot_risk_return(returns)

        # Exemplo de alocação de pesos (substitua pelos pesos reais que você deseja usar)
        weights = [40, 35, 25]  # Porcentagem de alocação para GOOGL, AAPL e MSFT
        weights = np.array(weights) / np.sum(weights) * 100  # Normaliza para porcentagem

        plot_weight_allocation(tickers, weights)

        # Gráfico de evolução dos retornos e risco
        plot_return_risk_over_time(data)
    else:
        print("Nenhum dado encontrado. Por favor, verifique os símbolos das ações ou a faixa de datas.")

if __name__ == "__main__":
    main()
#feito por Adriel Val, estudante de ciência da computação. 
#https://www.linkedin.com/in/adriel-val-31074516a/