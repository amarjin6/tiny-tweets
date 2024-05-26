import React, {useState} from "react";
import SideLink from "../components/SideLink";
import UserBox from "../components/UserBox";
import {
    BookmarksIcon,
    ExploreIcon,
    HomeIcon,
    ListsIcon,
    MoreIcon,
    NotificationsIcon,
    ProfileIcon,
} from "../icons/Icon";
import twitterLogo from "../images/twitter.svg";
import {useNavigate} from "react-router-dom";
import {useSelector} from "react-redux";

const sideLinks = [
    {
        name: "Home",
        icon: HomeIcon,
    },
    {
        name: "Explore",
        icon: ExploreIcon,
    },
    {
        name: "Statistic",
        icon: NotificationsIcon,
    },
    {
        name: "Bookmarks",
        icon: BookmarksIcon,
    },
    {
        name: "Lists",
        icon: ListsIcon,
    },
    {
        name: "Profile",
        icon: ProfileIcon,
    },
    {
        name: "More",
        icon: MoreIcon,
    },
];

const Sidebar = () => {
    const [active, setActive] = useState("Home");

    const currentUser = useSelector(state => state.reduxSlice.currentUser)

    const navigate = useNavigate()

    const handleMenuItemClick = (name) => {
        setActive(name);
        switch (name) {
            case "Home":
                navigate("/");
                break;
            case "Explore":
                navigate("/");
                break;
            case "Statistic":
                navigate("/statistic");
                break;
            case "Bookmarks":
                navigate("/");
                break;
            case "Lists":
                navigate("/");
                break;
            case "Profile":
                navigate("/" + currentUser);
                break;
            case "More":
                navigate("/");
                break;
            default:
                navigate("/");
        }
    };

    return (
        <div className="h-screen sticky top-0 flex flex-col justify-between w-72 px-2">
            <div>
                <div
                    className="mt-3 mb-2 ml-1 flex items-center justify-center w-12 h-12 rounded-full hover:bg-gray-lightest transform transition-colors duration-200">
                    <img src={twitterLogo} alt="Twitter Logo" className="w-20 h-20"/>
                </div>
                <nav className="mb-4">
                    <ul>
                        {sideLinks.map(({name, icon}) => (
                            <SideLink
                                key={name}
                                name={name}
                                Icon={icon}
                                active={active}
                                onMenuItemClick={handleMenuItemClick}
                            />
                        ))}
                    </ul>
                </nav>
                <div className="mt-2 mb-2 text-center">
                    <div className="bg-gray-600 hover:bg-blue-600 text-white font-bold shadow-lg rounded-full py-3 px-8 w-11/12 transform transition-colors duration-200">
                        <a
                            href="mailto:amarjin6@gmail.com?subject=Tiny Tweets Proposal">
                            Share Thoughts
                        </a>
                    </div>
                </div>

                <div className="mt-2 mb-2">
                    <button
                        className="bg-gray-600 hover:bg-green-600 text-white font-bold shadow-lg rounded-full py-3 px-8 w-11/12 transform transition-colors duration-200"
                        onClick={() => window.open("https://github.com/amarjin6/", "_blank")}>
                        Contact Us
                    </button>
                </div>

                <div className="mt-2 mb-2">
                    <button
                        className="bg-gray-600 hover:bg-red-600 text-white font-bold shadow-lg rounded-full py-3 px-8 w-11/12 transform transition-colors duration-200"
                        onClick={() => window.open("https://github.com/amarjin6/innotter/", "_blank")}>
                        Contribute
                    </button>
                </div>
            </div>
            <UserBox/>
        </div>
    );
};

export default Sidebar;
