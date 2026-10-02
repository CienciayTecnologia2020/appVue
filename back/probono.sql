-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 22 août 2024 à 10:33
-- Version du serveur : 10.4.32-MariaDB
-- Version de PHP : 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `probono`
--

-- --------------------------------------------------------

--
-- Structure de la table `attribute`
--

CREATE TABLE `attribute` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `attribute`
--

INSERT INTO `attribute` (`id`, `name`) VALUES
(1, 'Accuracy'),
(2, 'Execution speed'),
(3, 'Confidentiality'),
(4, 'Learnability');

-- --------------------------------------------------------

--
-- Structure de la table `building`
--

CREATE TABLE `building` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gps` varchar(255) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `version` int(11) DEFAULT NULL,
  `lifecycle_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `building`
--

INSERT INTO `building` (`id`, `name`, `description`, `address`, `gps`, `filename`, `date`, `version`, `lifecycle_id`) VALUES
(1, 'Building 1', 'Description for building 1', 'Address 1', 'GPS 1', 'file1.txt', '2023-01-01', 1, 1),
(2, 'BuildingDD 2', 'Description for building 2', 'Address 2', 'GPS 2', 'file2_todo.txt', NULL, 1, NULL),
(4, '', '', '', '', '', '0000-00-00', 0, NULL),
(5, 'Building ', 'Description building 5', 'Address 5', 'GPS 5', 'file5.txt', NULL, 1, NULL),
(9, 'Building 55', '', '', '', '', NULL, 0, NULL),
(11, 'Kitchen 2.0', 'The Kitchen 2.0 will be housed in ?the former boiler house and laundry ?and will, as now, function as Aarhus University\'s entrepreneurial factory, where students and researchers ?can bridge the gap between research and business.', '', '', '', NULL, 0, NULL),
(12, 'NEW ONE', '', '', '', '', NULL, 0, NULL),
(13, 'Building 1850', '', '', '', '', NULL, 0, NULL),
(14, 'Chagge', '', '', '', '', '0000-00-00', 0, NULL),
(15, 'Viborg', '', '', '', '', NULL, 0, NULL),
(16, 'Building 24A', '', '', '', '', '0000-00-00', 0, NULL),
(17, 'Road N6', '', '', '', '', '0000-00-00', 0, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `building_filebim`
--

CREATE TABLE `building_filebim` (
  `building_id` int(11) NOT NULL,
  `fileBIM_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `building_filebim`
--

INSERT INTO `building_filebim` (`building_id`, `fileBIM_id`) VALUES
(1, 4),
(2, 4);

-- --------------------------------------------------------

--
-- Structure de la table `calculationfrequency`
--

CREATE TABLE `calculationfrequency` (
  `id` int(11) NOT NULL,
  `frequency` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `calculationfrequency`
--

INSERT INTO `calculationfrequency` (`id`, `frequency`) VALUES
(1, 'daily'),
(2, 'weekly'),
(3, 'monthly'),
(4, 'quarterly');

-- --------------------------------------------------------

--
-- Structure de la table `filebim`
--

CREATE TABLE `filebim` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `version` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `filebim`
--

INSERT INTO `filebim` (`id`, `name`, `date`, `version`) VALUES
(1, 'StructuralModel', '2024-01-01', 'v1.0'),
(2, 'ArchitecturalDesign', '2024-02-01', 'v1.1'),
(3, 'MEPModel', '2024-03-01', 'v2.0'),
(4, 'FacadeDesign', '2024-04-01', 'v1.2');

-- --------------------------------------------------------

--
-- Structure de la table `kpi`
--

CREATE TABLE `kpi` (
  `id` int(11) NOT NULL,
  `calculationfrequency_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `impact` text DEFAULT NULL,
  `baseLineDataNeeded` text DEFAULT NULL,
  `responsibilityDefinition` text DEFAULT NULL,
  `responsibilityCalculation` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `dataRequirements` text DEFAULT NULL,
  `formula` text DEFAULT NULL,
  `pillar` varchar(255) DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `kpi`
--

INSERT INTO `kpi` (`id`, `calculationfrequency_id`, `name`, `impact`, `baseLineDataNeeded`, `responsibilityDefinition`, `responsibilityCalculation`, `description`, `dataRequirements`, `formula`, `pillar`, `unit`) VALUES
(1, 1, ' Amount of reused material', '', 'False', '', '', 'For the evaluation of reused materials in the buildings, the materials reuse- or recycling potential \nshould be evaluated and specified. It could be divided into: \n- Landfill.\n- Material utilization, i.e. as road-fill or similar. \n- Material recycling.\n- Direct reuse or upcycling', '', '', 'Environmental', '%'),
(2, 1, ' Number of EPDs or material-specific data being linked to the new project', '', 'False', '', '', '% of materials/products in the project having EPD or relevant material specific data.\nIn general, but especially in relation to reused materials, it is important to link relevant materials \nspecific information into the new projects.', '', '', 'Environmenta', 'TBD'),
(3, 1, 'Expected remaining life of materials/building/GBN', '', 'False', '', '', 'Estimated remaining lifetime of specific material or the whole building/GBN.\nThe remaining lifetime and expected maintenance is of interest, especially when working with reused \nmaterials (but also in relation to operation cost and maintenance/replacement)', '', '', 'Environmental', 'years '),
(4, 1, 'Consumption of drinking water', '', 'False', '', '', 'm³ of drinking quality water used in the building/GBN.\nReducing the drinking water consumption reduces the operation cost and the pressure on the natural \nwater cycle.', '', '', 'Environmental', 'm^3'),
(5, 1, 'Discharge of waste water', '', 'False', '', '', 'm³ of waste water discharged from the building/GBN.\nReducing the discharge of waste water reduces the operation cost and the pressure on the natural \nwater cycle.', '', '', 'Environmental', 'm^3'),
(6, 1, ' Service life of novel materials', '', 'False', '', '', 'Estimated durability of the materials without performance loss, in years.\n', '', '', 'Environmental', 'years '),
(7, 1, 'Roof cooling efficiency of the outdoor environment', '', 'True', '', '', 'Experimental determination: Surface temperature of at least 2 positions free of remote shading of \nthe roof before retrofitting.\nnumerical simulation: \n- Albedo and Thermal Emissivity of the roof before retrofitting (taking 3 samples from a 200 x 200 test \nspecimen)\n- Weather data (temperature, radiation, relative humidity, etc.).\n- Occupancy schedule vs. Temperature set-points.\n- Energy consumption submetered on last floor.\n- Building envelope geometry and thermal & physical values of layers.', '', 'Energy simulations\nor\nOn-site measurements - monitoring systems\n?FRout = 100 * (Qoref -Qo)/Qoref\nQo, the transmitted heat to the urban environment', 'Environmental', '% or kWh/m2 ·y'),
(8, 1, 'Roof energy cooling efficiency', '', 'True', '', '', 'Experimental determination: Surface temperature of at least 2 positions free of remote shading of \nthe roof before retrofitting.\nNumerical simulation:\n--> For roof-centred innovation, necessity of investigating specifically last floor “Thermal zone”, in \norder to attribute properly the benefits from the retrofitting actions. Sub-metering of last floor would \nhelp.\n--> A temperature sensor on this last floor could also allow to correct the measured energy \nconsumption from the eventual changes in building usages.\n--> Occupant schedules estimate (per rooms).\n· Weather data (temperature, radiation, relative humidity, etc.)\n- occupancy schedule vs. Temperature set-points\n- Energy consumption sub-metered on last floor\n- Building envelope geometry and thermal and physical values of layer', '', 'Energy simulations\nor\nOn-site measurements - monitoring systems\n?CEP = 100 * (CEP, ref -CEP)/CEP, ref\nCEP: Primary energy consumption', 'Energy', '% or kWh/m2 ·y'),
(9, 1, 'Roof cooling efficiency for the indoor environment', '', 'True', '', '', 'Mitigation potential of thermal discomfort during the cooling season. The cooling season is the period in which the building presents cooling needs and may vary according to the climate and the passive \nsolution implemented. This efficiency is computed only for the occupied periods and based on the degree-hours (DH) according to the adaptive thermal comfort standard (EN 16798).\n', '', 'Energy simulations \nor\nOn-site measurements - monitoring systems\n? FRin = 100 * (DHref -DH)/Dhref\nDH, degree.hour on the summer period according to standard EN 16978', 'Energy', '% or °C.h '),
(10, 1, ' Electricity generation capacity installed within the LL (capacity per source)', '', 'True', '', '', 'Type of power plant with resource used and its nominal power', '', '', 'Energy', 'MWel '),
(11, 1, ' Heat generation capacity installed within the LL (capacity per source)', '', 'True', '', '', 'Type of heat generation plant with resource used and its nominal heating power', '', '', 'Energy', 'MWth'),
(12, 1, 'Cold generation capacity installed within the LL (capacity per source)', '', 'True', '', '', 'Type of cold generation plant with resource used and its nominal cooling power', '', '', 'Energy', 'MWth'),
(13, 1, ' Electrical storage capacity installed within the LL', '', 'True', '', '', 'Type battery installed and its capacity', '', '', 'Energy', 'kWhel '),
(14, 1, 'Thermal storage capacity installed within the LL', '', 'True', '', '', 'Type of thermal storage and its capacity', '', '', 'Energy', 'kWhth'),
(15, 1, ' Share of heat consumer connected to the district heating system', '', 'True', '', '', 'Share of heat consumer connected to the district heating system\n', '', '', 'Energy', '%'),
(16, 1, ' Share of cold consumer connected to the district cooling system', '', 'True', '', '', 'Share of cold consumer connected to the district cooling system\n', '', '', 'Energy', '%'),
(17, 1, ' Energy demand supplied the renewable energy storage system', '', 'True', '', '', 'Amount of energy demand covered by the renewable energy storage system\n', '', '', 'Energy', 'kWh'),
(18, 1, 'Energy saved thanks to bidirectional charging system', '', 'True', '', '', 'Amount of primary energy not demanded from the network due to the deployment of bidirectional charging solutions', '', '', 'Energy', 'kWh '),
(19, 1, ' RESS capacity vs. Energy storage ratio', '', 'False', '', '', 'This indicator evaluates the performance and usefulness (in practical operation) of the Renewable \nEnergy Storage System (RESS), by establishing the ratio between the total capacities of the RESS system versus the energy effectively stored.', '', 'On-site measurements - monitoring systems', 'Energy', '%'),
(20, 1, ' CO2 savings due to the use of recycled materials', '', 'True', '', '', 'This indicator aims at quantifying the CO2 emissions saved due to the use of recycled materials (plastic, composite) in GBN buildings, instead of petrol-derived (\"primary\") ones.', '', 'BIM, LCA', 'Environmenta', 'kgCO2eq'),
(21, 1, 'CO2 emissions per MWh of primary energy consumed in the GBN', '', 'True', '', '', 'This indicator characterizes the CO2 emissions associated to the energy mix feeding the GBN (both imported from the network and produced within the GBN).', '', 'Energy bills\n', 'Environmental', 'kgCO2eq ');

-- --------------------------------------------------------

--
-- Structure de la table `kpi_lifecycle`
--

CREATE TABLE `kpi_lifecycle` (
  `kpi_id` int(11) NOT NULL,
  `lifecycle_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `kpi_lifecycle`
--

INSERT INTO `kpi_lifecycle` (`kpi_id`, `lifecycle_id`) VALUES
(1, 3),
(1, 4),
(2, 2),
(3, 3),
(4, 3),
(5, 3),
(6, 2),
(6, 3),
(7, 3),
(8, 3),
(9, 3),
(10, 3),
(11, 3),
(12, 3),
(13, 3),
(14, 3),
(15, 3),
(16, 3),
(17, 3),
(18, 3),
(19, 3),
(20, 2),
(21, 3);

-- --------------------------------------------------------

--
-- Structure de la table `lifecycle`
--

CREATE TABLE `lifecycle` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `lifecycle`
--

INSERT INTO `lifecycle` (`id`, `name`) VALUES
(1, 'Product Stage'),
(2, 'Construction Stage'),
(3, 'Use'),
(4, 'End of Life'),
(5, 'Beyond the Building Life Cycle');

-- --------------------------------------------------------

--
-- Structure de la table `location`
--

CREATE TABLE `location` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `latitude` decimal(10,8) NOT NULL,
  `longitude` decimal(11,8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `location`
--

INSERT INTO `location` (`id`, `name`, `image`, `description`, `latitude`, `longitude`) VALUES
(1, 'Aarhus LivingLab', 'https://static.dezeen.com/uploads/2022/11/aarhus-school-of-architecture-adept_dezeen_2364_sq_0-852x852.jpg', 'Aarhus LL is located in a section of Aarhus University called the University City (in Danish: Universitetsbyen). The University city contains buildings, which previously have been housing a hospital. Through refurbishment, the buildings are being converted to support an extended range of activities related to the academic life at Aarhus University. Buildings 23, 24, 1850, 1830, 1810, and 1790 have been chosen as focal points for the LL.', 56.16290000, 10.15000000),
(2, 'Madrid LivingLab', 'https://conferences.au.dk/fileadmin/_processed_/5/a/csm_IMG_0324__Joergen_Weber_luftfoto_b076b90e7d.jpg', 'Other Living Lab info and description', 40.41680000, -3.70380000),
(3, 'Dublin LivingLab', NULL, NULL, 53.35014000, -6.26615500);

-- --------------------------------------------------------

--
-- Structure de la table `location_building`
--

CREATE TABLE `location_building` (
  `general_id` int(11) NOT NULL,
  `building_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `location_building`
--

INSERT INTO `location_building` (`general_id`, `building_id`) VALUES
(1, 11),
(1, 13),
(1, 15),
(1, 16),
(1, 17),
(2, 5),
(2, 9),
(2, 12),
(2, 14);

-- --------------------------------------------------------

--
-- Structure de la table `modelchoice`
--

CREATE TABLE `modelchoice` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `text` varchar(255) NOT NULL,
  `problem_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `modelchoice`
--

INSERT INTO `modelchoice` (`id`, `text`, `problem_id`) VALUES
(1, 'The simulation does not include acoustics', 1),
(3, 'The simulation model the physics of thermal fluids', 1),
(4, 'Geometries are simplified, removing small scale details and focusing on thermal impact', 1),
(8, 'Other modeling', 2),
(9, 'Modeling in CFD', 8),
(10, 'Must include accoustics physics', 8);

-- --------------------------------------------------------

--
-- Structure de la table `objective`
--

CREATE TABLE `objective` (
  `id` int(11) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `objective`
--

INSERT INTO `objective` (`id`, `description`) VALUES
(1, 'Analyze an on-going situation using measured data'),
(2, 'Predict performance or behaviors in a given scenario'),
(3, 'Predict performance or behaviors in multiple scenarios'),
(4, 'Find an optimum'),
(5, 'Check that a threshold is respected');

-- --------------------------------------------------------

--
-- Structure de la table `output`
--

CREATE TABLE `output` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `math_relation` varchar(255) NOT NULL,
  `threshold` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `output`
--

INSERT INTO `output` (`id`, `name`, `math_relation`, `threshold`) VALUES
(1, 'Minimum temperature', '>=', '18°'),
(3, '12', '00', '12°'),
(4, 'Output', '>', '12');

-- --------------------------------------------------------

--
-- Structure de la table `parameter`
--

CREATE TABLE `parameter` (
  `id` int(11) NOT NULL,
  `value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `problem`
--

CREATE TABLE `problem` (
  `id` int(11) NOT NULL,
  `need` text NOT NULL,
  `estimation_type` enum('Quantitative','Qualitative') DEFAULT NULL,
  `accepted_risk` varchar(255) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem`
--

INSERT INTO `problem` (`id`, `need`, `estimation_type`, `accepted_risk`, `context_id`) VALUES
(1, 'We want to improve thermal comfort in a building that we renovate, with a new ventilation system, taking into account internal and external factors (weather, windows opened, etc.).', 'Quantitative', 'mouseX: 95, mouseY: 3', 1),
(2, 'Need for better stakeholder engagement, and any', 'Quantitative', 'mouseX: 61, mouseY: 14', 1),
(3, 'Need for accurate KPI tracking', 'Quantitative', 'mouseX: 94, mouseY: 6', 1),
(4, 'Need for contextual analysis in urban planning', 'Quantitative', 'mouseX: 85, mouseY: 11', 1),
(5, 'We want to improve thermal comfort in a building under renovation, with a new ventilation system, taking into account factors like weather, doors opened or closed, etc.', NULL, 'mouseX: 0, mouseY: 0', 1);

-- --------------------------------------------------------

--
-- Structure de la table `problem_building`
--

CREATE TABLE `problem_building` (
  `problem_id` int(11) NOT NULL,
  `building_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem_building`
--

INSERT INTO `problem_building` (`problem_id`, `building_id`) VALUES
(1, 5),
(1, 9),
(1, 11),
(2, 5),
(5, 11),
(5, 15),
(5, 17);

-- --------------------------------------------------------

--
-- Structure de la table `problem_kpi`
--

CREATE TABLE `problem_kpi` (
  `problem_id` int(11) NOT NULL,
  `kpi_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem_kpi`
--

INSERT INTO `problem_kpi` (`problem_id`, `kpi_id`) VALUES
(1, 18),
(1, 19);

-- --------------------------------------------------------

--
-- Structure de la table `problem_objective`
--

CREATE TABLE `problem_objective` (
  `problem_id` int(11) NOT NULL,
  `objective_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem_objective`
--

INSERT INTO `problem_objective` (`problem_id`, `objective_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 2),
(2, 3),
(2, 4),
(2, 5),
(3, 1),
(3, 2),
(3, 3),
(3, 4),
(3, 5),
(4, 1),
(4, 5);

-- --------------------------------------------------------

--
-- Structure de la table `problem_output`
--

CREATE TABLE `problem_output` (
  `problem_id` int(11) NOT NULL,
  `output_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem_output`
--

INSERT INTO `problem_output` (`problem_id`, `output_id`) VALUES
(2, 1),
(2, 3),
(3, 4);

-- --------------------------------------------------------

--
-- Structure de la table `problem_parameter`
--

CREATE TABLE `problem_parameter` (
  `problem_id` int(11) NOT NULL,
  `parameter_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `problem_scenario`
--

CREATE TABLE `problem_scenario` (
  `problem_id` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `problem_stakeholder`
--

CREATE TABLE `problem_stakeholder` (
  `problem_id` int(11) NOT NULL,
  `stakeholder_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `problem_stakeholder`
--

INSERT INTO `problem_stakeholder` (`problem_id`, `stakeholder_id`) VALUES
(1, 1),
(1, 23),
(1, 24),
(2, 1),
(5, 14),
(5, 15),
(5, 18);

-- --------------------------------------------------------

--
-- Structure de la table `scenario`
--

CREATE TABLE `scenario` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `scenario_parameter`
--

CREATE TABLE `scenario_parameter` (
  `scenario_id` int(11) NOT NULL,
  `parameter_id` int(11) NOT NULL,
  `value` varchar(255) DEFAULT 'default_value',
  `uncertained` tinyint(1) DEFAULT 0,
  `optimized` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `stakeholder`
--

CREATE TABLE `stakeholder` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `specificities` varchar(255) DEFAULT NULL,
  `requirements` varchar(255) DEFAULT NULL,
  `general_description` text DEFAULT NULL,
  `related_kpi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `stakeholder`
--

INSERT INTO `stakeholder` (`id`, `name`, `specificities`, `requirements`, `general_description`, `related_kpi`) VALUES
(1, 'Architect1', NULL, NULL, NULL, NULL),
(4, 'Consultant', '', '', '', ''),
(5, 'Aarhus University Administration', 'Reviewed Stakeholder', 'Ensure energy efficiency improvements align with university policies and budget constraints.', 'The administrative body responsible for the overall management and operations of Aarhus University.', NULL),
(7, 'Students and Researchers', 'Reviewed Stakeholder', 'Maintain a comfortable indoor climate to support productivity and well-being, while minimizing disruptions during the renovation process.', 'Individuals who use the Kitchen 2.0 for entrepreneurial activities and research projects.', NULL),
(8, 'Aarhus University Administration', 'Reviewed Stakeholder', 'Ensure the renovation aligns with university policies, budget constraints, and long-term sustainability goals.', 'The administrative body responsible for overseeing the operations and development of Aarhus University.', NULL),
(9, 'Students and Researchers', 'Reviewed Stakeholder', 'Provide a comfortable and conducive environment for innovation and collaboration, including optimal thermal comfort and air quality.', 'Individuals who will use the Kitchen 2.0 for entrepreneurial and research activities.', NULL),
(10, 'Facilities Management', 'Reviewed Stakeholder', 'Implement a ventilation system that is easy to maintain, energy-efficient, and integrates well with existing building systems.', 'The team responsible for the maintenance and operation of university buildings and infrastructure.', NULL),
(13, 'Students and Researchers', 'Reviewed Stakeholder', 'Maintain a comfortable indoor climate to support productivity and well-being, considering factors like weather and door usage.', 'Individuals who will use the Kitchen 2.0 for entrepreneurial and research activities.', NULL),
(14, 'Aarhus University Administration', 'Reviewed Stakeholder', 'Ensure the renovation aligns with university policies, budget constraints, and long-term sustainability goals.', 'The administrative body responsible for the overall management and operation of Aarhus University.', NULL),
(15, 'Students and Researchers', 'Reviewed Stakeholder', 'Provide a comfortable and conducive environment for innovation, including optimal thermal comfort and air quality.', 'Individuals who will use the Kitchen 2.0 for entrepreneurial activities, bridging research and business.', NULL),
(18, 'New Stakeholder', 'Specificities', 'Requirements', 'General Description', 'Related KPI'),
(19, 'Aarhus University Students', 'Reviewed Stakeholder', 'Comfortable and eco-friendly study and work environments, access to modern amenities, and spaces that foster collaboration and innovation.', 'Students enrolled at Aarhus University who will use the facilities for academic and entrepreneurial activities.', NULL),
(22, 'University Administration', 'Reviewed Stakeholder', 'Efficient use of resources, alignment with the university\'s sustainability goals, and ensuring the facilities support the academic mission of the university.', 'The administrative body responsible for the management and operation of Aarhus University.', NULL),
(23, 'Aarhus University Administration', 'Reviewed Stakeholder', 'Ensure the renovation aligns with university policies, budget constraints, and long-term sustainability goals.', 'The administrative body responsible for the overall management and operations of Aarhus University.', NULL),
(24, 'Students and Researchers', 'Reviewed Stakeholder', 'Provide a comfortable and conducive environment for innovation and collaboration, including optimal thermal comfort and air quality.', 'Individuals who will use the Kitchen 2.0 for entrepreneurial and research activities.', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `testrequirements`
--

CREATE TABLE `testrequirements` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `attribute_id` int(11) DEFAULT NULL,
  `text` varchar(255) NOT NULL,
  `problem_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `testrequirements`
--

INSERT INTO `testrequirements` (`id`, `attribute_id`, `text`, `problem_id`) VALUES
(2, 2, 'The simulation shall provide results in less that 5 minutes', 1),
(3, 3, 'The simulation shall require the transfer of data outside the simulation', 1),
(4, 4, 'The simulation shall be usable by architects', 1),
(11, 1, 'The simulation shall be sufficiently accurate to prove that the temperature requirement is satisfied', 1),
(17, 2, 'Less than 5 minutes', 2),
(20, 2, 'More speed', 2),
(22, 2, 'Must be run in a few minutes on a laptop', 8);

-- --------------------------------------------------------

--
-- Structure de la table `verification`
--

CREATE TABLE `verification` (
  `id` int(11) NOT NULL,
  `aspect` varchar(255) NOT NULL,
  `note` text NOT NULL,
  `date` date NOT NULL,
  `id_problem` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

--
-- Déchargement des données de la table `verification`
--

INSERT INTO `verification` (`id`, `aspect`, `note`, `date`, `id_problem`) VALUES
(1, 'Aspect 1', 'This is a test note for aspect 1', '1970-01-30', 1),
(2, 'Aspect 2', 'This is a test note for aspect 2', '2023-06-28', 1),
(3, 'Aspect 3', 'This is a test note for aspect 3', '0000-00-00', 2);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `attribute`
--
ALTER TABLE `attribute`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `building`
--
ALTER TABLE `building`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_lifecycle` (`lifecycle_id`);

--
-- Index pour la table `building_filebim`
--
ALTER TABLE `building_filebim`
  ADD PRIMARY KEY (`building_id`,`fileBIM_id`),
  ADD KEY `fileBIM_id` (`fileBIM_id`);

--
-- Index pour la table `calculationfrequency`
--
ALTER TABLE `calculationfrequency`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `filebim`
--
ALTER TABLE `filebim`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `kpi`
--
ALTER TABLE `kpi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `calculationfrequency_id` (`calculationfrequency_id`);

--
-- Index pour la table `kpi_lifecycle`
--
ALTER TABLE `kpi_lifecycle`
  ADD PRIMARY KEY (`kpi_id`,`lifecycle_id`),
  ADD KEY `lifeCycle_id` (`lifecycle_id`);

--
-- Index pour la table `lifecycle`
--
ALTER TABLE `lifecycle`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `location_building`
--
ALTER TABLE `location_building`
  ADD UNIQUE KEY `general_id` (`general_id`,`building_id`),
  ADD KEY `building_id` (`building_id`);

--
-- Index pour la table `modelchoice`
--
ALTER TABLE `modelchoice`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `objective`
--
ALTER TABLE `objective`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `output`
--
ALTER TABLE `output`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `parameter`
--
ALTER TABLE `parameter`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `problem`
--
ALTER TABLE `problem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_context_id` (`context_id`);

--
-- Index pour la table `problem_building`
--
ALTER TABLE `problem_building`
  ADD PRIMARY KEY (`problem_id`,`building_id`),
  ADD KEY `building_id` (`building_id`);

--
-- Index pour la table `problem_kpi`
--
ALTER TABLE `problem_kpi`
  ADD PRIMARY KEY (`problem_id`,`kpi_id`),
  ADD KEY `kpi_id` (`kpi_id`);

--
-- Index pour la table `problem_objective`
--
ALTER TABLE `problem_objective`
  ADD PRIMARY KEY (`problem_id`,`objective_id`),
  ADD KEY `objective_id` (`objective_id`);

--
-- Index pour la table `problem_output`
--
ALTER TABLE `problem_output`
  ADD PRIMARY KEY (`problem_id`,`output_id`),
  ADD KEY `output_id` (`output_id`);

--
-- Index pour la table `problem_parameter`
--
ALTER TABLE `problem_parameter`
  ADD PRIMARY KEY (`problem_id`,`parameter_id`),
  ADD KEY `parameter_id` (`parameter_id`);

--
-- Index pour la table `problem_scenario`
--
ALTER TABLE `problem_scenario`
  ADD PRIMARY KEY (`problem_id`,`scenario_id`),
  ADD KEY `scenario_id` (`scenario_id`);

--
-- Index pour la table `problem_stakeholder`
--
ALTER TABLE `problem_stakeholder`
  ADD PRIMARY KEY (`problem_id`,`stakeholder_id`),
  ADD KEY `stakeholder_id` (`stakeholder_id`);

--
-- Index pour la table `scenario`
--
ALTER TABLE `scenario`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `scenario_parameter`
--
ALTER TABLE `scenario_parameter`
  ADD PRIMARY KEY (`scenario_id`,`parameter_id`),
  ADD KEY `parameter_id` (`parameter_id`);

--
-- Index pour la table `stakeholder`
--
ALTER TABLE `stakeholder`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `testrequirements`
--
ALTER TABLE `testrequirements`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `verification`
--
ALTER TABLE `verification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_problem` (`id_problem`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `attribute`
--
ALTER TABLE `attribute`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `building`
--
ALTER TABLE `building`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT pour la table `filebim`
--
ALTER TABLE `filebim`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `lifecycle`
--
ALTER TABLE `lifecycle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `modelchoice`
--
ALTER TABLE `modelchoice`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `objective`
--
ALTER TABLE `objective`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT pour la table `output`
--
ALTER TABLE `output`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `parameter`
--
ALTER TABLE `parameter`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=781;

--
-- AUTO_INCREMENT pour la table `problem`
--
ALTER TABLE `problem`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT pour la table `scenario`
--
ALTER TABLE `scenario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=378;

--
-- AUTO_INCREMENT pour la table `testrequirements`
--
ALTER TABLE `testrequirements`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT pour la table `verification`
--
ALTER TABLE `verification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `building`
--
ALTER TABLE `building`
  ADD CONSTRAINT `fk_lifecycle` FOREIGN KEY (`lifecycle_id`) REFERENCES `lifecycle` (`id`);

--
-- Contraintes pour la table `building_filebim`
--
ALTER TABLE `building_filebim`
  ADD CONSTRAINT `building_filebim_ibfk_1` FOREIGN KEY (`building_id`) REFERENCES `building` (`id`),
  ADD CONSTRAINT `building_filebim_ibfk_2` FOREIGN KEY (`fileBIM_id`) REFERENCES `filebim` (`id`);

--
-- Contraintes pour la table `kpi`
--
ALTER TABLE `kpi`
  ADD CONSTRAINT `kpi_ibfk_3` FOREIGN KEY (`calculationfrequency_id`) REFERENCES `calculationfrequency` (`id`);

--
-- Contraintes pour la table `kpi_lifecycle`
--
ALTER TABLE `kpi_lifecycle`
  ADD CONSTRAINT `kpi_lifecycle_ibfk_1` FOREIGN KEY (`kpi_id`) REFERENCES `kpi` (`id`),
  ADD CONSTRAINT `kpi_lifecycle_ibfk_2` FOREIGN KEY (`lifeCycle_id`) REFERENCES `lifecycle` (`id`);

--
-- Contraintes pour la table `location_building`
--
ALTER TABLE `location_building`
  ADD CONSTRAINT `location_building_ibfk_1` FOREIGN KEY (`general_id`) REFERENCES `location` (`id`),
  ADD CONSTRAINT `location_building_ibfk_2` FOREIGN KEY (`building_id`) REFERENCES `building` (`id`);

--
-- Contraintes pour la table `problem`
--
ALTER TABLE `problem`
  ADD CONSTRAINT `fk_context_id` FOREIGN KEY (`context_id`) REFERENCES `location` (`id`);

--
-- Contraintes pour la table `problem_building`
--
ALTER TABLE `problem_building`
  ADD CONSTRAINT `problem_building_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_building_ibfk_2` FOREIGN KEY (`building_id`) REFERENCES `building` (`id`);

--
-- Contraintes pour la table `problem_kpi`
--
ALTER TABLE `problem_kpi`
  ADD CONSTRAINT `problem_kpi_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_kpi_ibfk_2` FOREIGN KEY (`kpi_id`) REFERENCES `kpi` (`id`);

--
-- Contraintes pour la table `problem_objective`
--
ALTER TABLE `problem_objective`
  ADD CONSTRAINT `problem_objective_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_objective_ibfk_2` FOREIGN KEY (`objective_id`) REFERENCES `objective` (`id`);

--
-- Contraintes pour la table `problem_output`
--
ALTER TABLE `problem_output`
  ADD CONSTRAINT `problem_output_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_output_ibfk_2` FOREIGN KEY (`output_id`) REFERENCES `output` (`id`);

--
-- Contraintes pour la table `problem_parameter`
--
ALTER TABLE `problem_parameter`
  ADD CONSTRAINT `problem_parameter_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_parameter_ibfk_2` FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`id`);

--
-- Contraintes pour la table `problem_scenario`
--
ALTER TABLE `problem_scenario`
  ADD CONSTRAINT `problem_scenario_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_scenario_ibfk_2` FOREIGN KEY (`scenario_id`) REFERENCES `scenario` (`id`);

--
-- Contraintes pour la table `problem_stakeholder`
--
ALTER TABLE `problem_stakeholder`
  ADD CONSTRAINT `problem_stakeholder_ibfk_1` FOREIGN KEY (`problem_id`) REFERENCES `problem` (`id`),
  ADD CONSTRAINT `problem_stakeholder_ibfk_2` FOREIGN KEY (`stakeholder_id`) REFERENCES `stakeholder` (`id`);

--
-- Contraintes pour la table `scenario_parameter`
--
ALTER TABLE `scenario_parameter`
  ADD CONSTRAINT `scenario_parameter_ibfk_1` FOREIGN KEY (`scenario_id`) REFERENCES `scenario` (`id`),
  ADD CONSTRAINT `scenario_parameter_ibfk_2` FOREIGN KEY (`parameter_id`) REFERENCES `parameter` (`id`);

--
-- Contraintes pour la table `verification`
--
ALTER TABLE `verification`
  ADD CONSTRAINT `verification_ibfk_1` FOREIGN KEY (`id_problem`) REFERENCES `problem` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
