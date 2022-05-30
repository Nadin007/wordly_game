import React from "react";
import { StatisticBtn } from "./statisticBtn";
import './header.css'

export const Header = (props) => {
    return <header>
        <span className="header-title">Wordly</span>
        <StatisticBtn />
    </header>
}