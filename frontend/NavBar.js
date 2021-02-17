import React from "react";
import { StyleSheet, Text, View } from "react-native";

import TabBar from "./TabBar";

const NavBar = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>PosFix</Text>
      <TabBar />
    </View>
  );
};

export default NavBar;

const colors = { primary: "#05386B", secondary: "#5CDB95" };

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: {
    marginLeft: 30,
    marginTop: 10,
    color: colors.primary,
    fontSize: 30,
    fontWeight: "700",
  },
});
