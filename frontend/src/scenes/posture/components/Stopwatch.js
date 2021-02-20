import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";
import { useGlobalContext } from "../../../../context";
import Button from "./Button";
import useFirestore from "../../../../useFirestore";

const Stopwatch = ({ navigation, setIsStarted }) => {
  const [notifOpacity, setNotifOpacity] = useState(false);
  const { stopwatch, stopStopwatch } = useGlobalContext();
  const { docs } = useFirestore("notification");

  useEffect(() => {
    setNotifOpacity(true);
    const timeout = setTimeout(() => {
      // console.log("false");
      setNotifOpacity(0);
    }, 5000);
    return () => clearTimeout(timeout);
  }, [docs]);

  const getTimeMins = (seconds) => {
    const minutes = parseInt(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}m ${secs}s`;
  };

  const handleStop = () => {
    stopStopwatch();
    setIsStarted(false);
    navigation.navigate("Data");
  };

  return (
    <View style={styles.container}>
      <View
        style={
          notifOpacity ? styles.notifContainer : styles.notifContainerInvisible
        }
      >
        <Text style={styles.notif}>{docs && docs.message}</Text>
      </View>
      <View style={styles.circleContainer}>
        <Text style={styles.time}>{getTimeMins(stopwatch)}</Text>
      </View>
      <Button
        text="Finish"
        primary={true}
        handlePress={handleStop}
        style={styles.finishBtn}
      />
    </View>
  );
};

export default Stopwatch;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginHorizontal: 40,
    // justifyContent: "center",
  },
  notifContainer: {
    marginTop: 20,
    marginBottom: 40,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
    backgroundColor: Colors.TERTIARY,
  },
  notifContainerInvisible: {
    marginTop: 20,
    marginBottom: 40,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 10,
    backgroundColor: Colors.TERTIARY,
    opacity: 1,
  },
  notif: {
    textAlign: "center",
    color: Colors.PRIMARY,
    fontSize: 20,
    fontWeight: "500",
  },
  circleContainer: {
    height: 300,
    width: 300,
    alignSelf: "center",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    borderColor: Colors.PRIMARY,
    borderRadius: 150,
  },
  time: {
    color: Colors.PRIMARY,
    fontSize: 40,
  },
  finishBtn: {
    marginTop: 20,
    alignSelf: "center",
  },
});
