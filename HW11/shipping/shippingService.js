const { Kafka } = require("kafkajs");
const connectDB = require("./db");
const Shipping = require("./models/shippingModel");

const kafka = new Kafka({ clientId: "shipping", brokers: ["localhost:9092"] });
const consumer = kafka.consumer({ groupId: "shipping-group" });

async function start() {
    await connectDB();
    await consumer.connect();
    await consumer.subscribe({ topic: "order-confirmed", fromBeginning: true });

    await consumer.run({
        eachMessage: async ({ message }) => {
            const msg = JSON.parse(message.value.toString());
            console.log("Received order-confirmed message:", msg);

            const { itemId, itemName, quantity } = msg;

            const trackingId = `SHIP-${itemId}-${Math.floor(Math.random() * 10000)}`;

            const newShipment = await Shipping.create({
                itemId,
                itemName,
                quantity,
                trackingId,
                status: "pending",
            });

            console.log("Shipping record created:", newShipment);
        },
    });
}

start();