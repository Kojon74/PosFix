import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";

const PerformanceBar = ({ percent }) => {
  return (
    <View>
      <View style={styles.progressOuter}>
        <View
          style={{
            height: `${percent}%`,
            width: "100%",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: Colors.PRIMARY,
          }}
        >
          <Text style={styles.percentLabel}>{`${percent}%`}</Text>
        </View>
      </View>
    </View>
  );
};

export default PerformanceBar;

const styles = StyleSheet.create({
  progressOuter: {
    height: 150,
    width: 75,
    justifyContent: "flex-end",
    backgroundColor: Colors.TERTIARY,
  },
  percentLabel: {
    color: Colors.TERTIARY,
    fontSize: 20,
    fontWeight: "800",
  },
});
