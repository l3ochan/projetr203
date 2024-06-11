<?php
include 'config/db_connector.php';
?>

<?php
$query = "SELECT * FROM `data`";
$stmt = $conn->prepare($query);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows == 0) {
    // Afficher un message si aucun véhicule n'est associé à l'utilisateur
    echo "<p>Aucune valeur météorologiue trouvée.</p>";
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>La météo - SAE23</title>
    <link rel="stylesheet" href="weather.css">
</head>
<body>
    <h1 class="page-title">Avez vous donc vu la météo ?</h1>
    <div class="separator"></div>
    <table>
        <thead>
            <tr>
                <th>Ville</th>
                <th>Température</th>
                <th>Ressenti</th>
                <th>Température max</th>
                <th>Température min</th>
                <th>Pression barométrique</th>
                <th>Taux d'humidité</th>
                <th>Date & heure</th>
            </tr>
        </thead>
        <tbody>
            <?php while ($row = $result->fetch_assoc()) : ?>
                <tr>
                    <td><?= htmlspecialchars($row['name']) ?></td>
                    <td><?= htmlspecialchars($row['temp']) ?>°C</td>
                    <td><?= htmlspecialchars($row['feels_like']) ?>°C</td>
                    <td><?= htmlspecialchars($row['temp_min']) ?>°C</td>
                    <td><?= htmlspecialchars($row['temp_max']) ?>°C</td>
                    <td><?= htmlspecialchars($row['pressure']) ?> hpa</td>
                    <td><?= htmlspecialchars($row['humidity']) ?>%</td>
                    <td><?= htmlspecialchars($row['date_of_creation']) ?></td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>