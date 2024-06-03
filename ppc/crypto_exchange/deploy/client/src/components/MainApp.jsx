import {useEffect, useState} from "react";
import {baseRequest} from "../api/api";

const MainApp = () => {
    const [balance, setBalance] = useState("");
    const [info, setInfo] = useState("Набери 10000 монет для покупки флага");
    const [cards, setCards] = useState([]);
    const [disabled, setDisabled] = useState(false);

    const getBalance = () => {
        baseRequest
            .get("/balance")
            .then((event) => {
                setBalance(event.data.balance.toFixed(2));
            })
            .catch((error) => {
                console.log(error);
            });
    };

    const getCryptoCards = () => {
        baseRequest
            .get("/crypto_cards")
            .then((result) => {
                let arr = result.data;
                for (let index = 0; index < arr.length; index++) {
                    baseRequest
                        .get(`/get_amount_card?card_id=${arr[index].id}`)
                        .then((res) => {
                            arr[index].amount = 0;
                            if (!res.data.status_code) {
                                console.log(res.data.amount);
                                arr[index].amount = res.data.amount;
                            } else {
                                console.log(0);
                                arr[index].amount = 0;
                            }
                            if (index == arr.length - 1) {
                                setCards(arr);
                            }
                        });
                }
            })
            .catch((error) => console.log(error));

    };

    const buyCrypto = ({name}) => {
        baseRequest
            .post(`/buy_crypto?crypto_card_name=${name}`)
            .then((result) => {
                setInfo(result.data);
                getBalance();
                getCryptoCards();
            })
            .catch((error) => setInfo(error.response.data.detail));

    };

    const sellCrypto = ({name}) => {
        baseRequest
            .post(`/sell_crypto?crypto_card_name=${name}`)
            .then((result) => {
                setInfo(result.data);
                getBalance();
                getCryptoCards();
            })
            .catch((error) => setInfo(error.response.data.detail));
    };

    const buyFlag = () => {
        baseRequest
            .post("/by_flag")
            .then((result) => {
                setInfo(result.data.flag);
            })
            .catch((error) => {
                console.log(error);
                setInfo(error.response.data.detail)
            });
    };

    useEffect(() => {
        getBalance();
        getCryptoCards();
    }, []);

    return (
        <>
            <h1 className="heading">
                Balance: <strong>{balance}</strong> $
            </h1>
            <h1 className="info">{info}</h1>
            <button className="keyButton" onClick={buyFlag}>
                BUY KEY
            </button>
            <div className="container">
                {cards &&
                    cards.map((card) => {
                        return (
                            <div className="cryptoBody" key={card.id}>
                                <h2>{card.name}</h2>
                                <h2>{card.amount || 0}</h2>
                                <div>
                                    <button
                                        onClick={() =>
                                            buyCrypto({
                                                name: card.name,
                                            })
                                        }
                                        disabled={disabled}
                                    >
                                        buy
                                    </button>
                                    <p>
                                        <strong>{card.price_buy.toFixed(2)}</strong>
                                        <br/>
                                        <strong>{card.price_sell.toFixed(2)}</strong>
                                    </p>
                                    <button
                                        onClick={() => {
                                            sellCrypto({
                                                name: card.name,
                                            });
                                        }}
                                        disabled={disabled}
                                    >
                                        sell
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                {/* <div className="cryptoBody">
          <h2>Heading</h2>
          <div>
            <button>buy</button>
            <p>
              <strong>покупка</strong>
              <br />
              <strong>продажа</strong>
            </p>
            <button>sell</button>
          </div>
        </div> */}
            </div>
        </>
    );
};

export default MainApp;
