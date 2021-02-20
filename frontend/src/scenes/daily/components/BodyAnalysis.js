import React from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import { BODY_OUTLINE } from "../../../assets";
import { Colors } from "../../../styles";

const BodyAnalysis = () => {
  return (
    <View style={styles.container}>
      <Image style={styles.image} source={BODY_OUTLINE} />
      <View style={styles.analysis}>
        <Text style={styles.area}>Neck Curvature</Text>
        <Text style={styles.feedback}>Okay</Text>
        <Text style={styles.area}>Shoulder Impingement</Text>
        <Text style={styles.feedback}>Great</Text>
        <Text style={styles.area}>Back Curvature</Text>
        <Text style={styles.feedback}>Bad</Text>
        <View style={styles.tipContainer}>
          <Text style={styles.header}>Tips</Text>
          <Text style={styles.content}>
            Watch some athlene-x.com. Start by being aware of your posture and
            checking your posture every 20 mins.
          </Text>
        </View>
      </View>
    </View>
  );
};

export default BodyAnalysis;

const styles = StyleSheet.create({
  container: {
    height: "auto",
    marginHorizontal: 40,
    // paddingVertical: 10,
    flexDirection: "row",
    justifyContent: "space-around",
    borderBottomWidth: 1,
    borderBottomColor: Colors.PRIMARY,
  },
  image: { flex: 1, marginVertical: -20, height: "auto" },
  analysis: { flex: 2 },
  area: {
    marginVertical: 10,
    color: Colors.PRIMARY,
    fontSize: 18,
    fontWeight: "600",
  },
  feedback: {
    alignSelf: "flex-end",
    color: Colors.TERTIARY,
    fontSize: 20,
    fontWeight: "600",
  },
  tipContainer: {
    marginTop: 15,
    padding: 10,
    borderRadius: 10,
    backgroundColor: Colors.TERTIARY,
  },
  header: {
    marginBottom: 10,
    color: Colors.PRIMARY,
    fontSize: 20,
    fontWeight: "700",
  },
});
